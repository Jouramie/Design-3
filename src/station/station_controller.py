import subprocess
import threading
import time
from logging import Logger

import numpy as np

from src.d3_network.command import Command
from src.d3_network.network_exception import MessageNotReceivedYet
from src.d3_network.server_network_controller import ServerNetworkController
from src.domain.country_loader import CountryLoader
from src.domain.environments.navigation_environment import NavigationEnvironment
from src.domain.environments.real_world_environment_factory import RealWorldEnvironmentFactory
from src.domain.objects.color import Color
from src.domain.objects.flag_cube import FlagCube
from src.domain.path_calculator.direction import Direction
from src.domain.path_calculator.grid import Grid
from src.domain.path_calculator.action import Forward, Backward, Rotate, Right, Left, Grab, Drop, LightItUp, IR, Start
from src.domain.path_calculator.action import Movement
from src.domain.path_calculator.path_calculator import PathCalculator
from src.domain.path_calculator.path_converter import PathConverter
from src.vision.camera import Camera
from src.vision.robot_detector import RobotDetector
from src.vision.world_vision import WorldVision
from .station_model import StationModel


class StationController(object):
    DISTANCE_FROM_CUBE = NavigationEnvironment.BIGGEST_ROBOT_RADIUS + 5

    def __init__(self, model: StationModel, network: ServerNetworkController, camera: Camera,
                 real_world_environment_factory: RealWorldEnvironmentFactory, robot_detector: RobotDetector,
                 logger: Logger, config: dict):
        self._model = model
        self.__logger = logger
        self.__config = config
        self.__network = network

        self.__camera = camera

        self.__country_loader = CountryLoader(config)
        self.__world_vision = WorldVision(logger, config)
        self.__path_calculator = PathCalculator(logger)
        self.__path_converter = PathConverter(logger.getChild("PathConverter"))
        self.__navigation_environment = NavigationEnvironment(logger.getChild("NavigationEnvironment"))
        self.__navigation_environment.create_grid()

        self.__real_world_environment_factory = real_world_environment_factory
        self.__robot_detector = robot_detector

        self._model.world_camera_is_on = True

        def start_robot_thread():
            self.__logger.info('Updating robot.')
            subprocess.call("./src/scripts/boot_robot.bash", shell=True)

        self.__robot_thread = threading.Thread(None, start_robot_thread, name='Robot')

    def start_robot(self):
        self._model.robot_is_started = True
        self._model.start_time = time.time()

        if self.__config['robot']['update_robot']:
            self.__robot_thread.start()

        self.__logger.info("Waiting for robot to connect.")
        self.__network.host_network()
        self.__network.send_action(Start())
        # self.interactive_testing()

    def interactive_testing(self):
        while True:
            command = input('enter something:ir, grab, drop, light, forward, backward, rotate')
            command = command.split(" ")
            self.__logger.info('You entered : {}'.format(command[0]))

            if command[0] == 'ir':
                self.__network.send_action(IR())
                self.__check_infrared_signal()
            elif command[0] == 'grab':
                self.__network.send_action(Grab())
            elif command[0] == 'drop':
                self.__network.send_action(Drop())
            elif command[0] == 'led':
                self.__network.send_action(LightItUp())
            elif command[0] == 'f':
                self.__network.send_move_command(Forward(float(command[1])))
            elif command[0] == 'r':
                self.__network.send_move_command(Right(float(command[1])))
            elif command[0] == 'l':
                self.__network.send_move_command(Left(float(command[1])))
            elif command[0] == 'b':
                self.__network.send_move_command(Backward(float(command[1])))
            elif command[0] == 'r':
                self.__network.send_move_command(Rotate(float(command[1])))

    def __check_infrared_signal(self) -> int:
        try:
            return self.__network.check_received_infrared_signal()
        except MessageNotReceivedYet:
            return None

    def __find_country(self):
        self._model.country = self.__country_loader.get_country(self._model.country_code)
        self.__logger.info(
            "Found " + str(self._model.country) + " flag: " + str(self._model.country.stylized_flag.flag_cubes))

    def __select_next_cube_color(self):
        cube_index = self._model.current_cube_index
        while cube_index < 9:
            flag_cube = self._model.country.stylized_flag.flag_cubes[cube_index]
            if flag_cube.color is not Color.TRANSPARENT:
                self._model.current_cube_index = cube_index + 1
                self._model.next_cube = flag_cube
                self.__logger.info("New cube color {}".format(self._model.next_cube.color.name))
                break
            else:
                cube_index = cube_index + 1
        if cube_index >= 9:
            self._model.flag_is_finish = True

    def update(self):
        self._model.frame = self.__camera.get_frame()
        self._model.robot = self.__robot_detector.detect(self._model.frame)

        if self._model.robot is not None:
            robot_center_3d = self._model.robot.get_center_3d()
            self._model.real_path.append(np.float32(robot_center_3d))

        if not self._model.robot_is_started:
            return

        self._model.passed_time = time.time() - self._model.start_time

        if self._model.real_world_environment is None:
            self.__generate_real_world_environments()

        if not self._model.infrared_signal_asked:
            self.__logger.info("Entering new step, asking country-code.")

            self.__move_to_infra_red_station()
            return

        if self._model.robot_is_moving or self._model.country_code is None:
            try:
                msg = self.__network.check_robot_feedback()
            except MessageNotReceivedYet:
                return

            # TODO Envoyer update de position ou envoyer la prochaine commande de déplacement/grab/drop
            if msg['command'] == Command.EXECUTED_ALL_REQUESTS:
                self._model.robot_is_moving = False
            elif msg['command'] == Command.INFRARED_SIGNAL:
                self._model.country_code = msg['country_code']
                self.__logger.info("Infrared signal received! {code}".format(code=self._model.country_code))
                self.__find_country()
                self.__select_next_cube_color()
                return
            else:
                self.__logger.warning('Received strange message from robot: {}'.format(str(msg)))
                return

        if not self._model.flag_is_finish:
            if self._model.robot_is_holding_cube:
                self.__logger.info("Entering new step, moving to target_zone to place cube.")

                self.__move_to_drop_cube()
            else:
                if self._model.robot_is_grabbing_cube:
                    self.__logger.info("Entering new step, moving to grab the cube.")

                    self.__grab_cube()

                else:
                    self.__logger.info("Entering new step, travel to the cube.")
                    self.__move_to_grab_cube()
        else:
            if self._model.light_is_lit:
                self.__logger.info("Entering new step, resetting for next flag.")
                self.__network.sned_action(LightItUp)
                pass
            else:
                self.__logger.info("Entering new step, exiting zone to light led.")

                # TODO Calculer le path vers l'exterieur de la zone
                # TODO Envoyer la commande de déplacement + led

                self.__network.send_action(LightItUp())

                self._model.robot_is_moving = True
                self._model.light_is_lit = True

    def __generate_real_world_environments(self):
        # self.camera.take_picture()
        self._model.vision_environment = self.__world_vision.create_environment(self._model.frame,
                                                                                self.__config['table_number'])
        self.__logger.info("Vision Environment:\n{}".format(str(self._model.vision_environment)))
        self._model.real_world_environment = self.__real_world_environment_factory.create_real_world_environment(
            self._model.vision_environment)

        if self._model.country is not None:
            for cube in self._model.country.stylized_flag.flag_cubes:
                if cube.is_placed:
                    self._model.real_world_environment.cubes.append(cube)

        self.__logger.info("Real Environment:\n{}".format(str(self._model.real_world_environment)))

        self.__generate_navigation_environment()

    def __generate_navigation_environment(self):
        self.__navigation_environment.create_grid()
        self.__navigation_environment.add_real_world_environment(self._model.real_world_environment)

    def __find_path(self, start_position: tuple, end_position: tuple, end_direction: Direction) -> ([Movement], list):
        self.__generate_navigation_environment()
        # TODO tirer une exception plutot qu'un boolean
        is_possible = self.__path_calculator.calculate_path(start_position, end_position,
                                                            self.__navigation_environment.get_grid())
        if not is_possible:
            self.__logger.warning("Path to destination {} is not possible.".format(end_position))
            return None, None

        movements, path_planned = self.__path_converter.convert_path(
            self.__path_calculator.get_calculated_path(), self._model.robot, end_direction)

        self.__logger.info("Path planned: {}".format(" ".join(str(mouv) for mouv in movements)))

        return movements, path_planned

    def __send_movement_commands(self, movements: [Movement]) -> None:
        self.__network.send_move_command(movements)

    def __find_robot(self) -> tuple:
        if self._model.robot is None:
            self.__logger.warning("Robot position is undefined. Waiting to know robot position to find path.")
            return None
        self.__logger.info("Robot: {}".format(self._model.robot))
        return self._model.robot.center

    def __find_safe_position_near_cube(self, target_cube: FlagCube) -> (tuple, Direction):
        if target_cube.center[1] < Grid.DEFAULT_OFFSET + 5:
            self.__logger.info("Le cube {} est en bas.".format(str(target_cube)))
            target_position = (int(target_cube.center[0]),
                               int(target_cube.center[1] + self.DISTANCE_FROM_CUBE))
            desired_direction = Direction.SOUTH
            pass
        elif target_cube.center[1] > NavigationEnvironment.DEFAULT_WIDTH + Grid.DEFAULT_OFFSET - 10:
            self.__logger.info("Le cube {} est en haut.".format(str(target_cube)))
            target_position = (int(target_cube.center[0]),
                               int(target_cube.center[1] - self.DISTANCE_FROM_CUBE))
            desired_direction = Direction.NORTH
            pass
        elif target_cube.center[0] > NavigationEnvironment.DEFAULT_HEIGHT + Grid.DEFAULT_OFFSET - 5:
            self.__logger.info("Le cube {} est au fond.".format(str(target_cube)))
            target_position = (int(target_cube.center[0] - self.DISTANCE_FROM_CUBE),
                               int(target_cube.center[1]))
            desired_direction = Direction.EAST
            pass
        else:
            self.__logger.warning("Le cube {} n'est pas à la bonne place.".format(str(target_cube)))
            return

        return target_position, desired_direction

    def __move_to_infra_red_station(self):
        start_position = self.__find_robot()
        end_position = (10, 10)
        end_direction = Direction.SOUTH_WEST
        movements, self._model.planned_path = self.__find_path(start_position, end_position, end_direction)

        self.__send_movement_commands(movements)

        self.__network.send_action(IR())
        self._model.robot_is_moving = True
        self._model.infrared_signal_asked = True

        # TODO move in the mock
        if self.__config['robot']['use_mocked_robot_detector']:
            self.__robot_detector.robot_position = end_position
            self.__robot_detector.robot_direction = Direction.SOUTH.angle

    def __move_to_grab_cube(self):
        self._model.target_cube = self._model.real_world_environment.find_cube(self._model.next_cube.color)
        if self._model.target_cube is None:
            self.__logger.warning("The target cube is None. Cannot continue, exiting.")
            return

        start_position = self.__find_robot()
        end_position, end_direction = self.__find_safe_position_near_cube(self._model.target_cube)

        movements, self._model.planned_path = self.__find_path(start_position, end_position, end_direction)

        if movements is None:
            return

        self.__send_movement_commands(movements)

        self._model.robot_is_moving = True
        self._model.robot_is_grabbing_cube = True

        # TODO move in the mock
        if self.__config['robot']['use_mocked_robot_detector']:
            self.__robot_detector.robot_position = end_position
            self.__robot_detector.robot_direction = end_direction.angle

    def __grab_cube(self):
        self._model.real_world_environment.cubes.remove(self._model.target_cube)
        self._model.target_cube = None

        self.__network.send_move_command(
            [Forward(self.DISTANCE_FROM_CUBE - self.__config['distance_between_robot_center_and_cube_center'])])
        self.__network.send_action(Grab())
        self.__network.send_move_command(
            [Backward(self.DISTANCE_FROM_CUBE - self.__config['distance_between_robot_center_and_cube_center'] + 1)])

        self._model.robot_is_moving = True
        self._model.robot_is_grabbing_cube = False
        self._model.robot_is_holding_cube = True

    def __find_where_to_place_cube(self) -> tuple:
        cube_destination = self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center
        target_position = (cube_destination[0] + self.__config['distance_between_robot_center_and_cube_center'],
                           cube_destination[1])
        self.__logger.info("Target position: {}".format(str(target_position)))

        return target_position

    def __move_to_drop_cube(self):
        start_position = self.__find_robot()

        end_position = self.__find_where_to_place_cube()

        movements, self._model.planned_path = self.__find_path(start_position, end_position, None)

        self.__send_movement_commands(movements)
        self.__network.send_action(Drop())

        distance_backward = self.DISTANCE_FROM_CUBE - self.__config['distance_between_robot_center_and_cube_center']
        self.__network.send_move_command(Backward(distance_backward))

        self.__logger.info("Dropping cube.")

        placed_cube = self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1]
        placed_cube.place_cube()
        self._model.real_world_environment.cubes.append(placed_cube)
        self.__select_next_cube_color()

        self._model.robot_is_moving = True
        self._model.robot_is_holding_cube = False

        if self.__config['robot']['use_mocked_robot_detector']:
            self.__robot_detector.robot_position = (end_position[0] + distance_backward, end_position[1])
            self.__robot_detector.robot_direction = Direction.WEST.angle
