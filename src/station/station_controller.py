import subprocess
import time

import cv2

from src.d3_network.network_exception import MessageNotReceivedYet
from src.d3_network.server_network_controller import ServerNetworkController
from src.domain.country_loader import CountryLoader
from .station_model import StationModel


class StationController(object):
    def __init__(self, model: StationModel, network: ServerNetworkController, logger, config):
        self.model = model
        self.countryLoader = CountryLoader(config)
        self.network = network
        self.logger = logger
        self.config = config

        self.model.frame = cv2.VideoCapture(0)
        self.model.world_camera_is_on = True

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

    def __find_country(self):
        try:
            countries = self.countryLoader.get_country_list()
            selected_country = countries[self.model.country_code]
            self.model.country = selected_country

        except FileNotFoundError:
            print("This countries doesn't exists")

    def __select_next_cube_color(self):
        stylized_flag = self.model.country.get_stylized_flag()
        cubes = stylized_flag.get_cube_list()
        for cube in cubes:
            color_name = cube.get_colour_name()
            if color_name != "TRANSPARENT":
                self.model.next_cube_color = color_name
                break

    def update(self):
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
