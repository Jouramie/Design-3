import subprocess
import numpy as np
import time

import cv2

from src.d3_network.network_exception import MessageNotReceivedYet
from src.d3_network.server_network_controller import ServerNetworkController
from src.domain.country_loader import CountryLoader
from src.vision.tableManager import TableManager
from src.vision.table import Table
from src.vision.coordinateConverter import CoordinateConverter
from src.vision.robotDetector import RobotDetector
from src.vision.frameDrawer import FrameDrawer
from .station_model import StationModel
from src.config import TABLE_NUMBER
from src.vision.camera import *


class StationController(object):
    def __init__(self, model: StationModel, network: ServerNetworkController, logger, config):
        self.model = model
        self.countryLoader = CountryLoader(config)
        self.table = self.set_table(TABLE_NUMBER)
        self.coord_converter = CoordinateConverter(self.table.world_to_camera)
        self.robot_detector = RobotDetector(self.table.camParam, self.coord_converter)
        self.frame_drawer = FrameDrawer(self.table.camParam, self.coord_converter)
        self.network = network
        self.logger = logger
        self.config = config
        self.camera = create_camera(1)

        self.model.world_camera_is_on = True

    def set_table(self, table_number) -> Table:
        table_manager = TableManager()
        table = table_manager.create_table(table_number)
        return table

    def start_robot(self):
        self.model.robot_is_started = True
        self.model.start_time = time.time()

        if self.config['update_robot']:
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
        if self.model.robot is not None:
            self.frame_drawer.drawRobot(frame, self.model.robot)
        if self.model.projected_path is not None:
            self.frame_drawer.draw_projected_path(frame, self.model.projected_path)
        if self.model.real_path is not None:
            self.frame_drawer.draw_real_path(frame, np.asarray(self.model.real_path))

    def __find_country(self):
        self.model.country = self.countryLoader.get_country(self.model.country_code)

    def __select_next_cube_color(self):
        stylized_flag = self.model.country.stylized_flag
        cubes = stylized_flag.get_cube_list()
        for cube in cubes:
            color_name = cube.get_colour_name()
            if color_name != "TRANSPARENT":
                self.model.next_cube_color = color_name
                break

    def update(self):
        frame = self.camera.get_frame()
        self.model.robot = self.robot_detector.detect(frame)
        if self.model.robot is not None:
            robot_center_array = [self.model.robot.center[0], self.model.robot.center[1], 0]
            self.model.real_path.append(np.float32(robot_center_array))
        self.__draw_environment(frame)
        self.model.frame = frame
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
                self.__select_next_cube_color()
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
