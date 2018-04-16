import subprocess
import threading
import time
from logging import Logger
from math import sqrt, ceil, floor

import numpy as np

from src.d3_network.command import Command
from src.d3_network.network_exception import MessageNotReceivedYet
from src.d3_network.server_network_controller import ServerNetworkController
from src.domain.country_loader import CountryLoader
from src.domain.environments.navigation_environment import NavigationEnvironment
from src.domain.environments.real_world_environment_factory import RealWorldEnvironmentFactory
from src.domain.objects.color import Color
from src.domain.objects.wall import Wall
from src.domain.path_calculator.action import Forward, Backward, Rotate, Right, Left, Grab, Drop, LightItUp, IR, Action, \
    CanIGrab, Movement
from src.domain.path_calculator.direction import Direction
from src.domain.path_calculator.path_calculator import PathCalculator
from src.domain.path_calculator.path_converter import PathConverter
from src.domain.path_calculator.path_simplifier import PathSimplifier
from src.vision.camera import Camera
from src.vision.robot_detector import RobotDetector
from src.vision.world_vision import WorldVision
from .state import State
from .station_model import StationModel


class StationController(object):
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
        self.__path_simplifier = PathSimplifier(self.__navigation_environment, self.__logger)

        self.__real_world_environment_factory = real_world_environment_factory
        self.__robot_detector = robot_detector

        self._model.world_camera_is_on = True

        self.__destination = None
        self.__movements_to_destination: [Movement] = []
        self.__todo_when_arrived_at_destination: [Action] = []

        def start_robot_thread():
            self.__logger.info('Updating robot.')
            subprocess.call("./src/scripts/boot_robot.bash", shell=True)

        self.__robot_thread = threading.Thread(None, start_robot_thread, name='Robot')

    def start_robot(self):
        self._model.current_state = State.GETTING_COUNTRY_CODE
        self._model.start_time = time.time()

        if self.__config['robot']['update_robot']:
            self.__robot_thread.start()

        self.__logger.info("Waiting for robot to connect.")
        self.__network.host_network()
        self.__network.send_start()
        # self.interactive_testing()

    def interactive_testing(self):
        while True:
            command = input('enter something:ir, grab, drop, light, forward, backward, rotate')
            command = command.split(" ")
            self.__logger.info('You entered : {}'.format(command[0]))

            if command[0] == 'ir':
                self.__network.send_actions([IR()])
                self.__check_infrared_signal()
            elif command[0] == 'grab':
                self.__network.send_actions([Grab()])
            elif command[0] == 'drop':
                self.__network.send_actions([Drop()])
            elif command[0] == 'led':
                self.__network.send_actions([LightItUp()])
            elif command[0] == 'f':
                self.__network.send_actions([Forward(float(command[1]))])
            elif command[0] == 'r':
                self.__network.send_actions([Right(float(command[1]))])
            elif command[0] == 'l':
                self.__network.send_actions([Left(float(command[1]))])
            elif command[0] == 'b':
                self.__network.send_actions([Backward(float(command[1]))])
            elif command[0] == 'ro':
                self.__network.send_actions([Rotate(float(command[1]))])

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
            self._model.next_cube = None

    def update(self):
        self._model.frame = self.__camera.get_frame()
        self._model.robot = self.__robot_detector.detect(self._model.frame)

        if self._model.robot is not None:
            robot_center_3d = self._model.robot.get_center_3d()
            self._model.real_path.append(np.float32(robot_center_3d))

        if self._model.current_state is State.NOT_STARTED:
            return

        self._model.passed_time = time.time() - self._model.start_time

        if self._model.real_world_environment is None:
            self.__generate_real_world_environments()

        if self._model.current_state is State.WORKING:
            try:
                msg = self.__network.check_robot_feedback()
            except MessageNotReceivedYet:
                return
            # input('Press enter to continue execution.')  # TODO
            if msg['command'] == Command.EXECUTED_ALL_REQUESTS:
                self.__update_path()
                self.__send_next_actions_commands()
                if self._model.current_state is State.WORKING:
                    return

            elif msg['command'] == Command.INFRARED_SIGNAL:
                self._model.country_code = msg['country_code']
                self.__logger.info("Infrared signal received! {code}".format(code=self._model.country_code))
                self.__find_country()
                self.__select_next_cube_color()
                return
            elif msg['command'] == Command.GRAB_CUBE_FAILURE:
                self.__destination = None
                self.__todo_when_arrived_at_destination = None
                self._model.current_state = State.ADJUSTING_IN_CUBE_REPOSITORY
                self._model.next_state = None
                return

            else:
                self.__logger.warning('Received strange message from robot: {}'.format(str(msg)))
                return

        self.__logger.info("ENTERING NEW STATE: {}.".format(self._model.current_state))

        if self._model.current_state is State.GETTING_COUNTRY_CODE:
            self.__move_to_infra_red_station()
            self._model.next_state = State.TRAVELING_TO_CUBE_REPOSITORY

        elif self._model.current_state is State.TRAVELING_TO_CUBE_REPOSITORY:
            self.__move_to_cube_area()
            self._model.next_state = State.ADJUSTING_IN_CUBE_REPOSITORY

        elif self._model.current_state is State.ADJUSTING_IN_CUBE_REPOSITORY:
            if not self.__is_correctly_oriented_for_cube_grab():
                self.__logger.info("Orienting robot.")
                self.__orientate_for_cube_grab()
            elif not self.__is_correctly_positioned_for_cube_grab():
                self.__logger.info("Strafing robot.")
                self.__strafing_for_cube_grab()
            else:
                self.__logger.info("Robot is correctly placed.")
                self._model.current_state = State.MOVING_TO_GRAB_CUBE
                return
            self._model.next_state = State.ADJUSTING_IN_CUBE_REPOSITORY

        elif self._model.current_state == State.MOVING_TO_GRAB_CUBE:
            self.__move_robot_to_grab_cube()
            self._model.next_state = State.GRABBING_CUBE

        elif self._model.current_state == State.GRABBING_CUBE:
            self.__grab_cube()
            self._model.next_state = State.MOVING_OUT_OF_DANGER_ZONE

        elif self._model.current_state == State.MOVING_OUT_OF_DANGER_ZONE:
            if self.__robot_move_to_safe_area_after_grabbing_cube():
                self._model.current_state = State.TRAVELLING_TO_CUBE_DEPOT
                return
            else:
                self._model.next_state = State.TRAVELLING_TO_CUBE_DEPOT

        elif self._model.current_state == State.TRAVELLING_TO_CUBE_DEPOT:
            self.__travel_to_cube_depot()
            self._model.next_state = State.ADJUSTING_IN_CUBE_DEPOT

        elif self._model.current_state == State.ADJUSTING_IN_CUBE_DEPOT:
            if not self.__is_correctly_oriented_for_cube_drop():
                self.__logger.info("Orienting robot.")
                self.__orientate_for_cube_drop()
            elif not self.__is_correctly_positioned_for_cube_drop():
                self.__logger.info("Strafing robot.")
                self.__strafing_for_cube_drop()
            elif not self.__is_correctly_aligned_for_cube_drop():
                self.__logger.info("Aligning robot.")
                self.__aligning_for_cube_drop()
            else:
                self.__logger.info("Robot is correctly placed.")
                self._model.current_state = State.DROP_CUBE
                return
            self._model.next_state = State.ADJUSTING_IN_CUBE_DEPOT

        elif self._model.current_state == State.DROP_CUBE:
            self.__drop_cube()
            if self._model.next_cube is None:
                self._model.next_state = State.EXITING_TARGET_ZONE_AND_LIGHT
            else:
                self._model.next_state = State.TRAVELING_TO_CUBE_REPOSITORY

        elif self._model.current_state == State.EXITING_TARGET_ZONE_AND_LIGHT:
            self.__travel_out_of_target_zone()

            self.__network.send_actions([LightItUp()])
            self._model.next_state = State.RESETTING

        elif self._model.current_state == State.RESETTING:
            self._model.current_state = State.NOT_STARTED
            return
        else:
            self.__logger.error('The state {} is not supported.'.format(self._model.current_state))

        self._model.current_state = State.WORKING

    def __robot_move_to_safe_area_after_grabbing_cube(self):
        safe_distance = 5
        safe_area = 5

        if self._model.robot.center[0] > (self.__navigation_environment.DEFAULT_HEIGHT +
                                          self.__navigation_environment.get_grid().DEFAULT_OFFSET -
                                          self.__navigation_environment.BIGGEST_ROBOT_RADIUS - safe_area -
                                          self.__navigation_environment.CUBE_HALF_SIZE * 2):
            if self._model.last_grabbed_cube.wall == Wall.MIDDLE:
                self.__todo_when_arrived_at_destination = [Backward(safe_distance / 2)]
            elif self._model.last_grabbed_cube.wall == Wall.UP:
                self.__todo_when_arrived_at_destination = [Left(safe_distance)]
            else:
                self.__todo_when_arrived_at_destination = [Right(safe_distance)]
        elif self._model.robot.center[1] < (self.__navigation_environment.get_grid().DEFAULT_OFFSET +
                                            self.__navigation_environment.BIGGEST_ROBOT_RADIUS + safe_area +
                                            self.__navigation_environment.CUBE_HALF_SIZE * 2):
            if self._model.last_grabbed_cube.wall == Wall.DOWN:
                self.__todo_when_arrived_at_destination = [Backward(safe_distance)]
            else:
                self.__todo_when_arrived_at_destination = [Left(safe_distance)]
        elif self._model.robot.center[1] > (self.__navigation_environment.DEFAULT_WIDTH +
                                            self.__navigation_environment.get_grid().DEFAULT_OFFSET -
                                            self.__navigation_environment.BIGGEST_ROBOT_RADIUS - safe_area -
                                            self.__navigation_environment.CUBE_HALF_SIZE * 2):
            if self._model.last_grabbed_cube.wall == Wall.UP:
                self.__todo_when_arrived_at_destination = [Backward(safe_distance)]
            else:
                self.__todo_when_arrived_at_destination = [Right(safe_distance)]
        else:
            self.__logger.info("Robot is in safe area, will start using PathCalculator")
            return True

        self.__logger.info("Moving to safe area with {}".format((str(self.__todo_when_arrived_at_destination))))
        self.__update_path(force=True)
        self.__send_next_actions_commands()

        return False

    def __is_correctly_oriented_for_cube_drop(self):
        return 175 < self._model.robot.orientation % 360 < 185

    def __is_correctly_oriented_for_cube_grab(self):
        if self._model.target_cube.wall == Wall.MIDDLE:
            return 5 > self._model.robot.orientation % 360 or 355 < self._model.robot.orientation % 360
        elif self._model.target_cube.wall == Wall.UP:
            return 85 < self._model.robot.orientation % 360 < 95
        elif self._model.target_cube.wall == Wall.DOWN:
            return 265 < self._model.robot.orientation % 360 < 275
        else:
            self.__logger.info("Wall_of_next_cube is not correctly set:\n{}".format(str(self._model.target_cube.wall)))
            return False

    def __strafing_for_cube_drop(self):
        self.__destination = None

        robot_pos_y = self._model.robot.center[1]
        if robot_pos_y > (self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center[1] + 1):
            distance = robot_pos_y - self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center[1]
            if distance < 3:
                distance = distance + 4
            self.__todo_when_arrived_at_destination = [Left(distance)]

        if robot_pos_y < (self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center[1] - 1):
            distance = self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center[1] - robot_pos_y
            if distance < 3:
                distance = distance + 4
            self.__todo_when_arrived_at_destination = [Right(distance)]

        self.__update_path(force=True)
        self.__send_next_actions_commands()

    def __strafing_for_cube_grab(self):
        robot_pos_x = self._model.robot.center[0]
        robot_pos_y = self._model.robot.center[1]

        self.__destination = None

        if self._model.target_cube.wall == Wall.UP:
            if robot_pos_x > (self._model.target_cube.center[0]):
                distance = robot_pos_x - self._model.target_cube.center[0]
                self.__todo_when_arrived_at_destination = [Left(distance)]

            if robot_pos_x < (self._model.target_cube.center[0]):
                distance = self._model.target_cube.center[0] - robot_pos_x
                self.__todo_when_arrived_at_destination = [Right(distance)]

        elif self._model.target_cube.wall == Wall.DOWN:
            if robot_pos_x > (self._model.target_cube.center[0]):
                distance = robot_pos_x - self._model.target_cube.center[0]
                self.__todo_when_arrived_at_destination = [Right(distance)]

            if robot_pos_x < (self._model.target_cube.center[0]):
                distance = self._model.target_cube.center[0] - robot_pos_x
                self.__todo_when_arrived_at_destination = [Left(distance)]

        elif self._model.target_cube.wall == Wall.MIDDLE:
            if robot_pos_y > (self._model.target_cube.center[1]):
                distance = robot_pos_y - self._model.target_cube.center[1]
                self.__todo_when_arrived_at_destination = [Right(distance)]

            if robot_pos_y < (self._model.target_cube.center[1]):
                distance = self._model.target_cube.center[1] - robot_pos_y
                self.__todo_when_arrived_at_destination = [Left(distance)]
        else:
            self.__logger.info("Wall_of_next_cube is not correctly set:\n{}".format(str(self._model.target_cube.wall)))
            return

        self.__update_path(force=True)
        self.__send_next_actions_commands()

    def __is_correctly_positioned_for_cube_drop(self):
        robot_pos_y = self._model.robot.center[1]
        target_position_y = int(self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center[1])
        return (target_position_y - 1) < robot_pos_y < (target_position_y + 1)

    def __is_correctly_positioned_for_cube_grab(self):
        robot_pos_x = self._model.robot.center[0]
        robot_pos_y = self._model.robot.center[1]

        if self._model.target_cube.wall == Wall.UP or self._model.target_cube.wall == Wall.DOWN:
            target_position_x = self._model.target_cube.center[0]
            return (target_position_x - 1) < robot_pos_x < (target_position_x + 1)

        elif self._model.target_cube.wall == Wall.MIDDLE:
            target_position_y = self._model.target_cube.center[1]
            return (target_position_y - 1) < robot_pos_y < (target_position_y + 1)

        else:
            self.__logger.info("Wall_of_next_cube is not correctly set:\n{}".format(str(self._model.target_cube.wall)))

    def __aligning_for_cube_drop(self):
        robot_pos = (self._model.robot.center[0], self._model.robot.center[1])
        target_position = (
            int(self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center[0]
                + self.__config['distance_between_robot_center_and_cube_center']),
            int(self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center[1]))

        distance_to_travel = calculate_distance_between_two_points(robot_pos, target_position)
        self.__logger.info("Moving to drop target : {} cm".format(str(distance_to_travel)))

        self.__destination = None
        if robot_pos[0] < target_position[0]:
            self.__todo_when_arrived_at_destination = [Backward(distance_to_travel)]
        else:
            self.__todo_when_arrived_at_destination = [Forward(distance_to_travel)]

        self.__update_path(force=True)
        self.__send_next_actions_commands()

    def __generate_real_world_environments(self):
        self.__camera.take_picture()
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

    def __find_path(self, end_position: tuple, end_direction: int) -> ([Movement], list):
        self.__logger.info("Finding path to {}".format((end_position, end_direction)))
        if end_position is not None:
            # TODO tirer une exception plutot qu'un boolean
            is_possible = self.__path_calculator.calculate_path(self._model.robot.center, end_position,
                                                                self.__navigation_environment.get_grid())
            if not is_possible:
                self.__logger.warning("Path to destination {} is not possible.".format(end_position))
                return None, None
            raw_path = self.__path_calculator.get_calculated_path()
        else:
            raw_path = []

        simplified_path = self.__path_simplifier.simplify(raw_path)
        self.__logger.debug('Simplified path: {}'.format(simplified_path))

        movements, path_planned = self.__path_converter.convert_path(simplified_path, self._model.robot, end_direction)

        self.__logger.info("Path planned: {}".format(" ".join(str(mouv) for mouv in movements)))

        return movements, path_planned

    def __send_next_actions_commands(self) -> None:
        if self.__movements_to_destination:
            actions_to_be_send: [Action] = [self.__movements_to_destination.pop(0)]
            if actions_to_be_send[0].command == Command.MOVE_ROTATE:
                if self.__movements_to_destination:
                    actions_to_be_send.append(self.__movements_to_destination.pop(0))

        elif self.__todo_when_arrived_at_destination:
            actions_to_be_send, self.__todo_when_arrived_at_destination = self.__todo_when_arrived_at_destination, []
        else:
            if self._model.next_state is not None:
                self._model.current_state, self._model.next_state = self._model.next_state, None
            return

        self.__network.send_actions(actions_to_be_send)

    def __find_safe_position_in_cube_area(self) -> (tuple, int):
        return (166, 33), None

    def __find_where_to_place_cube(self) -> tuple:
        cube_destination = self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center
        target_position = (cube_destination[0] + self.__config['distance_between_robot_center_and_cube_center'],
                           cube_destination[1])
        self.__logger.info("Target position: {}".format(str(target_position)))

        return target_position

    def __move_to_infra_red_station(self):
        self.__destination = None, 210
        self.__todo_when_arrived_at_destination = [IR()]

        self.__update_path(force=True)
        self.__send_next_actions_commands()

    def __orientate_for_cube_drop(self) -> None:
        self.__destination = None, Direction.WEST.angle
        self.__todo_when_arrived_at_destination = None

        self.__update_path(force=True)
        self.__send_next_actions_commands()

    def __orientate_for_cube_grab(self) -> None:
        if self._model.target_cube.wall == Wall.DOWN:
            self.__logger.info("Le cube {} est en bas.".format(str(self._model.target_cube)))
            self.__destination = None, Direction.SOUTH.angle
        elif self._model.target_cube.wall == Wall.UP:
            self.__logger.info("Le cube {} est en haut.".format(str(self._model.target_cube)))
            self.__destination = None, Direction.NORTH.angle
        elif self._model.target_cube.wall == Wall.MIDDLE:
            self.__logger.info("Le cube {} est au fond.".format(str(self._model.target_cube)))
            self.__destination = None, Direction.EAST.angle
        else:
            self.__logger.warning("Le cube {} n'est pas à la bonne place.".format(str(self._model.target_cube)))
            return

        self.__todo_when_arrived_at_destination = None

        self.__update_path(force=True)
        self.__send_next_actions_commands()

    def __move_to_cube_area(self):
        self._model.target_cube = self._model.real_world_environment.find_cube(self._model.next_cube.color)
        if self._model.target_cube is None:
            self.__logger.warning("The target cube is None. Cannot continue, exiting.")
            return

        self.__destination = self.__find_safe_position_in_cube_area()
        self.__todo_when_arrived_at_destination = None

        self.__update_path(force=True)
        self.__send_next_actions_commands()

    def __move_robot_to_grab_cube(self):
        robot_pos = (floor(self._model.robot.center[0]), floor(self._model.robot.center[1]))
        target_position = None
        if self._model.target_cube.wall == Wall.UP:
            target_position = (int(self._model.target_cube.center[0]),
                               int(self._model.target_cube.center[1] - self.__config[
                                   'distance_between_robot_center_and_cube_center']))

        elif self._model.target_cube.wall == Wall.DOWN:
            target_position = (int(self._model.target_cube.center[0]),
                               int(self._model.target_cube.center[1] + self.__config[
                                   'distance_between_robot_center_and_cube_center']))

        elif self._model.target_cube.wall == Wall.MIDDLE:
            target_position = (
                int(self._model.target_cube.center[0] - self.__config['distance_between_robot_center_and_cube_center']),
                int(self._model.target_cube.center[1]))

        distance_to_travel = calculate_distance_between_two_points(robot_pos, target_position)
        self.__logger.info("Moving to grab cube by : {} cm".format(str(distance_to_travel)))

        self.__destination = None
        self.__todo_when_arrived_at_destination = [Forward(distance_to_travel), CanIGrab()]

        self.__update_path(force=True)
        self.__send_next_actions_commands()

    def __grab_cube(self):
        self._model.last_grabbed_cube = self._model.target_cube
        self._model.real_world_environment.cubes.remove(self._model.target_cube)
        self._model.target_cube = None

        self.__destination = None
        self.__todo_when_arrived_at_destination = [Grab(), Backward(NavigationEnvironment.BIGGEST_ROBOT_RADIUS)]

        self.__update_path(force=True)
        self.__send_next_actions_commands()

    def __find_safe_position_to_place_cube(self) -> (tuple, int):
        cube_destination_x = self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center[0]
        target_position = None
        if self._model.current_cube_index <= 2:
            target_position = ((self.__config['distance_between_robot_center_and_cube_center']
                                + 10), 33)
        elif self._model.current_cube_index <= 5:
            target_position = ((self.__config['distance_between_robot_center_and_cube_center']
                                + cube_destination_x + 10), 33)
        elif self._model.current_cube_index <= 8:
            target_position = ((self.__config['distance_between_robot_center_and_cube_center']
                                + cube_destination_x + 10), 33)
        else:
            self.__logger.info("Target position is not valid")
        return target_position, None

    def __travel_to_cube_depot(self):
        self.__destination = self.__find_safe_position_to_place_cube()
        self.__todo_when_arrived_at_destination = None

        self.__update_path(force=True)
        self.__send_next_actions_commands()

    def __drop_cube(self):
        distance_backward = NavigationEnvironment.BIGGEST_ROBOT_RADIUS
        self.__todo_when_arrived_at_destination = [Drop(), Backward(distance_backward)]

        self.__update_path(force=True)
        self.__send_next_actions_commands()

        placed_cube = self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1]
        placed_cube.place_cube()
        self._model.real_world_environment.cubes.append(placed_cube)
        self.__select_next_cube_color()

    def __update_path(self, force: bool = False):
        if not force and not self.__movements_to_destination:
            return

        if not force and len(self.__movements_to_destination) == 1 and \
                self.__movements_to_destination[-1].command == Command.MOVE_ROTATE:
            return

        if force:
            self.__generate_navigation_environment()

        self.__logger.info('Destination : {}'.format(self.__destination))
        if self.__destination is not None:
            end_position, end_orientation = self.__destination

            movements, self._model.planned_path = self.__find_path(end_position, end_orientation)
            if movements is None:
                return
        else:
            movements = []

        self.__movements_to_destination = movements

    def __is_correctly_aligned_for_cube_drop(self):
        robot_pos_x = self._model.robot.center[0]
        target_position_x = int(
            self._model.country.stylized_flag.flag_cubes[self._model.current_cube_index - 1].center[0] +
            self.__config['distance_between_robot_center_and_cube_center'])
        return (target_position_x - 1) < robot_pos_x < (target_position_x + 1)

    def __travel_out_of_target_zone(self):
        target_left = (90, 60)
        target_center = (90, 30)
        target_right = (90, 0)
        if not self.__navigation_environment.get_grid().is_obstacle(target_left):
            self.__destination = target_left, None
        elif not self.__navigation_environment.get_grid().is_obstacle(target_center):
            self.__destination = target_center, None
        elif not self.__navigation_environment.get_grid().is_obstacle(target_right):
            self.__destination = target_right, None

        self.__todo_when_arrived_at_destination = None

        self.__update_path(force=True)
        self.__send_next_actions_commands()

def calculate_distance_between_two_points(point1: tuple, point2: tuple) -> int:
    distance_between_two_points = sqrt(
        (floor(point2[1]) - floor(point1[1])) ** 2 + floor((point2[0]) - floor(point1[0])) ** 2)
    ceil_distance_between_two_points = ceil(distance_between_two_points)

    return int(ceil_distance_between_two_points)

