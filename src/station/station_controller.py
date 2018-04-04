import subprocess
import time
from logging import Logger

import numpy as np

from src.d3_network.network_exception import MessageNotReceivedYet
from src.d3_network.server_network_controller import ServerNetworkController
from src.domain.country_loader import CountryLoader
from src.domain.environments.navigation_environment import NavigationEnvironment
from src.domain.environments.real_world_environment import RealWorldEnvironment
from src.domain.objects.color import Color
from src.domain.path_calculator.path_calculator import PathCalculator
from src.domain.path_calculator.path_converter import PathConverter
from src.vision.camera import Camera
from src.vision.coordinate_converter import CoordinateConverter
from src.vision.frame_drawer import FrameDrawer
from src.vision.robot_detector import RobotDetector
from src.vision.table_camera_configuration import TableCameraConfiguration
from src.vision.world_vision import WorldVision
from .station_model import StationModel


class StationController(object):
    def __init__(self, model: StationModel, network: ServerNetworkController, camera: Camera,
                 table_camera_config: TableCameraConfiguration, coordinate_converter: CoordinateConverter,
                 robot_detector: RobotDetector, logger: Logger, config: dict):
        self.model = model
        self.logger = logger
        self.config = config
        self.network = network

        self.camera = camera

        self.country_loader = CountryLoader(config)
        self.world_vision = WorldVision(logger, config)
        self.path_calculator = PathCalculator()
        self.path_converter = PathConverter(logger.getChild("PathConverter"))
        self.navigation_environment = NavigationEnvironment(logger.getChild("NavigationEnvironment"))
        self.navigation_environment.create_grid()

        self.table_camera_config = table_camera_config
        self.coordinate_converter = coordinate_converter
        self.robot_detector = robot_detector
        self.frame_drawer = FrameDrawer(self.table_camera_config.camera_parameters, self.coordinate_converter,
                                        logger.getChild("FrameDrawer"))

        self.obstacle_pos = []

        self.model.world_camera_is_on = True

    def start_robot(self):
        self.model.robot_is_started = True
        self.model.start_time = time.time()

        if self.config['robot']['update_robot']:
            subprocess.call("./src/scripts/boot_robot.bash", shell=True)

        self.logger.info("Waiting for robot to connect.")
        self.network.host_network()
        self.network.send_start_command()

    def __check_infrared_signal(self):
        try:
            return self.network.check_infrared_signal()
        except MessageNotReceivedYet:
            return None

    def __draw_environment(self, frame):
        if self.model.vision_environment is not None:
            self.frame_drawer.draw_vision_environment(frame, self.model.vision_environment)

        if self.model.real_world_environment is not None:
            self.frame_drawer.draw_real_world_environment(frame, self.model.real_world_environment)

        if self.model.planned_path is not None and self.model.planned_path:
            self.frame_drawer.draw_planned_path(frame, self.model.planned_path)

        if self.model.real_path is not None and self.model.real_path:
            self.frame_drawer.draw_real_path(frame, np.asarray(self.model.real_path))

        if self.model.robot is not None:
            self.frame_drawer.draw_robot(frame, self.model.robot)

        # TODO draw navigation grid

    def __find_country(self):
        self.model.country = self.country_loader.get_country(self.model.country_code)
        self.logger.info("Found " + str(self.model.country) + " flag: " + str(self.model.country.stylized_flag.flag_cubes))

    def __select_next_cube_color(self):
        cube_index = self.model.current_cube_index
        while cube_index < 9:
            flag_cube = self.model.country.stylized_flag.flag_cubes[cube_index]
            if flag_cube.color is not Color.TRANSPARENT:
                self.model.current_cube_index = cube_index + 1
                self.model.next_cube = flag_cube
                self.logger.info(
                    "Found " + str(self.model.country) + " flag: "
                    + str(self.model.country.stylized_flag.flag_cubes[cube_index]))
                break
            else:
                cube_index = cube_index + 1
        if cube_index >= 9:
            self.model.flag_is_finish = True

    def update(self):
        self.model.frame = self.camera.get_frame()
        self.model.robot = self.robot_detector.detect(self.model.frame)

        if self.model.robot is not None:
            robot_center_3d = self.model.robot.get_center_3d()
            self.model.real_path.append(np.float32(robot_center_3d))

        if not self.model.robot_is_started:
            self.__draw_environment(self.model.frame)
            return

        self.model.passed_time = time.time() - self.model.start_time

        if self.model.vision_environment is None:
            self.model.vision_environment = self.world_vision.create_environment(self.model.frame,
                                                                                 self.config['table_number'])
            self.logger.info("Vision Environment:\n{}".format(str(self.model.vision_environment)))

            self.model.real_world_environment = RealWorldEnvironment(self.model.vision_environment,
                                                                     self.coordinate_converter)
            self.logger.info("Real Environment:\n{}".format(str(self.model.real_world_environment)))

            self.navigation_environment.add_real_world_environment(self.model.real_world_environment)

        self.__draw_environment(self.model.frame)

        if not self.model.infrared_signal_asked:
            self.network.ask_infrared_signal()
            self.model.infrared_signal_asked = True
            return

        if self.model.country_code is None:
            country_received = self.__check_infrared_signal()

            if country_received is not None:
                self.model.country_code = country_received
                self.__find_country()
                self.__select_next_cube_color()
                target_cube = self.model.real_world_environment.find_cube(self.model.next_cube.color)
                if target_cube is None:
                    self.logger.warning("The target cube is None. Cannot continue, exiting.")
                    return

                if self.model.robot is None:
                    self.logger.warning("Robot position is undefined. Waiting to know robot position to find path.")
                    return

                target_position = (target_cube.center[0],
                                   target_cube.center[1] + max(self.model.robot.height, self.model.robot.width) + 10)
                is_possible = self.path_calculator.calculate_path(
                    self.model.robot.center, target_position, self.navigation_environment.get_grid())

                if not is_possible:
                    self.logger.warning("Path to the cube is not possible.\n Target: {}".format(target_position))
                    return

                _, self.model.planned_path = self.path_converter.convert_path(
                    self.path_calculator.get_calculated_path())

            return

        """
        # Verifier message du robot
            # Si mouvement terminé
                # robot_is_moving = false

        # Si robot en mouvement
            # Envoyer update de position
            # return

        # Si il reste des cubes a placer
            # Sinon
                # Si cube dans préhenseur
                    # Calculer le path vers la place dans le drapeau
                    # Envoyer la commande de déplacement au robot
                    # robot_is_moving = true
                # Sinon
                    # Choisir un cube
                    # Calculer le path vers le cube
                    # Envoyer la commande de déplacement au robot
                    # robot_is_moving = true
        # Sinon
            # Si le robot a fini d'allumer la led
                # soft_reset model
            # Sinon
                # Calculer le path vers l'exterieur de la zone
                # Envoyer la commande de déplacement + led
                # robot_is_moving = true
        """
