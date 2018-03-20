import subprocess

import cv2

from src.d3_network.network_exception import MessageNotReceivedYet
from src.domain.country_loader import CountryLoader
from .station_model import StationModel
from src.d3_network.server_network_controller import NetworkController


class StationController(object):
    def __init__(self, model: StationModel, network: NetworkController, logger, config):
        self.model = model
        self.countryLoader = CountryLoader(config)
        self.network = network
        self.logger = logger
        self.config = config

    def set_country_code(self, country_code):
        self.model.countryCode = country_code

    def start_timer(self):
        self.model.timer_is_on = True
        print("start timer")

    def start_robot(self):
        self.model.network_is_on = True

        if self.config['update_robot']:
            subprocess.call("./src/scripts/boot_robot.bash", shell=True)

        self.logger.info("Waiting for robot to connect.")
        self.network.host_network()
        self.network.send_start_command()

    def check_ir_signal(self):
        try:
            country_code = self.network.check_ir_signal()
        except MessageNotReceivedYet:
            return

        self.model.countryCode = country_code

    def select_country(self):
        try:
            countries = self.countryLoader.get_country_list()
            selected_country = countries[self.model.countryCode]
            self.model.country = selected_country

        except FileNotFoundError:
            print("This countries doesn't exists")

    def select_next_cube_color(self):
        stylized_flag = self.model.country.get_stylized_flag()
        cubes = stylized_flag.get_cube_list()
        for cube in cubes:
            color_name = cube.get_colour_name()
            if color_name != "TRANSPARENT":
                self.model.nextCubeColor = color_name
                break

    def select_frame(self):
        self.model.frame = cv2.VideoCapture(0)
        self.model.worldCamera_is_on = True

    def update(self):
        if not self.model.infrared_signal_asked:
            self.network.ask_ir_signal()
            self.model.infrared_signal_asked = True
            return

        if self.model.countryCode is None:
            country_received = False  # Check network if signal received

            if not country_received:
                return

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







