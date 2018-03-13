import subprocess

import cv2

from src.domain.country_loader import CountryLoader
from src.d3_network.network_exception import MessageNotReceivedYet


class StationController(object):
    def __init__(self, model, network, logger, config):
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

    def start_network(self):
        self.model.network_is_on = True

        if self.config['update_robot']:
            subprocess.call("./src/scripts/boot_robot.bash", shell=True)

        self.logger.info("Waiting for robot to connect.")
        self.network.host_network()
        self.network.send_start_command()
        self.network.ask_ir_signal()
        self.model.infrared_signal_asked = True

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
