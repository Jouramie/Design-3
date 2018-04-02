import subprocess
import time
from logging import Logger

import cv2
import numpy as np

from domain.path_calculator.path_converter import PathConverter
from src.d3_network.network_exception import MessageNotReceivedYet
from src.d3_network.server_network_controller import ServerNetworkController
from src.domain.color import Color
from src.domain.country_loader import CountryLoader
from src.domain.path_calculator.path_calculator import PathCalculator
from src.vision.camera import create_camera
from src.vision.coordinate_converter import CoordinateConverter
from src.vision.frame_drawer import FrameDrawer
from src.vision.robot_detector import RobotDetector
from src.vision.table_camera_configuration import TableCameraConfiguration
from src.vision.world_vision import DummyWorldVision
from .station_model import StationModel
from src.domain.navigation_environment import NavigationEnvironment
from src.vision.transform import Transform
from src.domain.vision_environment.obstacle import Obstacle
import operator


class StationController(object):
    def __init__(self, model: StationModel, network: ServerNetworkController,
                 table_camera_config: TableCameraConfiguration, logger: Logger, config: dict):
        self.model = model
        self.logger = logger
        self.config = config
        self.network = network

        self.camera = create_camera(config["camera_id"])

        self.country_loader = CountryLoader(config)
        self.world_vision = DummyWorldVision(self.camera)
        self.path_calculator = PathCalculator()
        self.path_converter = PathConverter()
        self.navigation_environment = NavigationEnvironment()
        self.navigation_environment.create_grid()

        self.table_camera_config = table_camera_config
        self.coordinate_converter = CoordinateConverter(self.table_camera_config.world_to_camera)
        self.robot_detector = RobotDetector(self.table_camera_config.cam_param, self.coordinate_converter)
        self.frame_drawer = FrameDrawer(self.table_camera_config.cam_param, self.coordinate_converter)

        self.obstacle_pos = []

        self.model.world_camera_is_on = True

    def start_robot(self):
        self.model.robot_is_started = True
        self.model.start_time = time.time()

        if self.config['update_robot']:
            subprocess.call("./src/scripts/boot_robot.bash", shell=True)

        self.model.vision_environment = self.world_vision.create_environment()

        for obstacle in self.model.vision_environment.obstacles:
            object_points = np.array([(0, 0, 41), (6.3, 0, 41), (-6.3, 0, 41), (0, 6.3, 41), (0, -6.3, 41)], 'float32')

            image_points = np.array([obstacle.center, (obstacle.center[0] + obstacle.radius, obstacle.center[1]),
                                     (obstacle.center[0] - obstacle.radius, obstacle.center[1]),
                                     (obstacle.center[0], obstacle.center[1] + obstacle.radius),
                                     (obstacle.center[0], obstacle.center[1] - obstacle.radius)])

            retval, rvec, tvec = cv2.solvePnP(object_points, image_points,
                                              self.table_camera_config.cam_param.camera_matrix,
                                              self.table_camera_config.cam_param.distortion)
            print(retval)

            camera_to_obstacle = Transform.from_parameters(np.asscalar(tvec[0]), np.asscalar(tvec[1]),
                                                           np.asscalar(tvec[2]), np.asscalar(rvec[0]),
                                                           np.asscalar(rvec[1]), np.asscalar(rvec[2]))
            world_to_obstacle = self.coordinate_converter.world_from_camera(camera_to_obstacle)

            robot_info = world_to_obstacle.to_parameters(True)
            obstacle_pos = (robot_info[0], robot_info[1])

            self.obstacle_pos.append(obstacle_pos)

            print("Position de l'obstacle = {}".format(str(obstacle_pos)))
            self.navigation_environment.add_obstacles(obstacle_pos)
            # TODO add obstacles to grid

        path = self.path_calculator.calculate_path((0, 0), (200, 0), self.navigation_environment.get_grid())
        _, self.model.planned_path = self.path_converter.convert_path(self.path_calculator.get_calculated_path())

        self.logger.info("Waiting for robot to connect.")
        # self.network.host_network()
        # self.network.send_start_command()

    def __check_infrared_signal(self):
        try:
            return 42  # self.network.check_infrared_signal()
        except MessageNotReceivedYet:
            return None

    def __draw_environment(self, frame):
        if self.model.robot is not None:
            # self.logger.info("Robot " + str(self.model.robot))
            self.frame_drawer.draw_robot(frame, self.model.robot)

        if self.model.planned_path is not None and self.model.planned_path:
            # self.logger.info("Planned path " + str(self.model.planned_path))
            self.frame_drawer.draw_planned_path(frame, self.model.planned_path)

        if self.model.real_path is not None and self.model.real_path:
            # self.logger.info("Real path " + str(self.model.real_path))
            self.frame_drawer.draw_real_path(frame, np.asarray(self.model.real_path))

        self.logger.info("Vision Environment: {}".format(str(self.model.vision_environment)))
        if self.model.vision_environment is not None:
            for obstacle in self.model.vision_environment.obstacles:
                self.frame_drawer.draw_obstacle(frame, obstacle)

            pass  # TODO draw environment

        for obstacle_pos in self.obstacle_pos:
            print(obstacle_pos)
            self.frame_drawer.draw_transformed_obstacle(frame, obstacle_pos)

        # TODO draw navigation grid

    def __find_country(self):
        self.model.country = self.country_loader.get_country(self.model.country_code)
        self.logger.info("Found " + str(self.model.country) + " flag: " + str(self.model.country.stylized_flag.colors))

    def __select_next_cube_color(self) -> None:
        """Choose the next color to be placed in the flag

        """

        # TODO pas retourner tout le temps le premier cube de couleur de la liste
        for color in self.model.country.stylized_flag.colors:
            if color is not Color.TRANSPARENT:
                self.model.next_cube_color = color
                break

    def update(self):
        # self.logger.info("StationController.update()")
        self.model.frame = frame = self.camera.get_frame()
        self.model.robot = self.robot_detector.detect(frame)

        if self.model.robot is not None:
            robot_center_3d = self.model.robot.get_center_3d()
            self.model.real_path.append(np.float32(robot_center_3d))

        self.__draw_environment(frame)

        if not self.model.robot_is_started:
            return

        self.model.passed_time = time.time() - self.model.start_time

        if not self.model.infrared_signal_asked:
            # self.network.ask_infrared_signal()
            self.model.infrared_signal_asked = True
            return

        if self.model.country_code is None:
            country_received = self.__check_infrared_signal()

            if country_received is not None:
                self.model.country_code = country_received
                self.__find_country()
                self.__select_next_cube_color()
                target_cube = self.model.vision_environment.find_cube(self.model.next_cube_color)
                # TODO find path to cube using path finding
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
