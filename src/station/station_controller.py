import subprocess
import time
from logging import Logger

import numpy as np

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

        self.table_camera_config = table_camera_config
        self.coord_converter = CoordinateConverter(self.table_camera_config.world_to_camera)
        self.robot_detector = RobotDetector(self.table_camera_config.cam_param, self.coord_converter)
        self.frame_drawer = FrameDrawer(self.table_camera_config.cam_param, self.coord_converter)

        self.model.world_camera_is_on = True

    def start_robot(self):
        self.model.robot_is_started = True
        self.model.start_time = time.time()

        if self.config['update_robot']:
            subprocess.call("./src/scripts/boot_robot.bash", shell=True)

        # TODO create navigation_environment

        self.logger.info("Waiting for robot to connect.")
        self.network.host_network()
        self.network.send_start_command()

    def __check_infrared_signal(self):
        try:
            return self.network.check_infrared_signal()
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

        if self.model.environment is not None:
            pass  # TODO draw environment

    def __find_country(self):
        self.model.country = self.country_loader.get_country(self.model.country_code)
        self.logger.info("Found " + str(self.model.country) + " flag: " + str(self.model.country.stylized_flag.flag_cubes))

    def select_next_cube_color(self):
        cube_index = self.model.current_cube_index
        flag_cube = self.model.country.stylized_flag.flag_cubes[cube_index]
        if flag_cube.color is not Color.TRANSPARENT:
            self.model.current_cube_index = cube_index + 1
            self.model.next_cube = flag_cube
        else:
            self.model.current_cube_index = cube_index + 1
            self.select_next_cube_color()

    def update(self):
        # self.logger.info("StationController.update()")
        self.model.frame = frame = self.camera.get_frame()
        self.model.robot = self.robot_detector.detect(frame)
        self.model.environment = self.world_vision.create_environment()

        if self.model.robot is not None:
            robot_center_3d = self.model.robot.get_center_3d()
            self.model.real_path.append(np.float32(robot_center_3d))

        self.__draw_environment(frame)

        if not self.model.robot_is_started:
            return

        self.model.passed_time = time.time() - self.model.start_time

        if not self.model.infrared_signal_asked:
            self.network.ask_infrared_signal()
            self.model.infrared_signal_asked = True
            return

        if self.model.country_code is None:
            country_received = self.__check_infrared_signal()

            if country_received is not None:
                self.model.country_code = country_received
                self.__find_country()
                self.select_next_cube_color()
                self.model.environment.find_cube(self.model.next_cube.color)
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
