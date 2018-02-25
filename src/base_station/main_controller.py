import logging
import os
import time

from src.domain.environment import Environment
from src.domain.path_calculator.path_calculator import PathCalculator
from src.config import MAIN_CONTROLLER_LOG_DIR, MAIN_CONTROLLER_LOG_FILE


class MainController(object):

    __environment = 0
    __path_calculator = 0

    def __init__(self, log_level=logging.INFO):
        self.__initialize_log(log_level)
        self.__environment = Environment()
        self.__path_calculator = PathCalculator()

    def create_environment(self, obstacles_point):
        # call world_vision.create_environment()
        # find some way to feed size from point to graph
        self.__environment.create_graph()
        self.__environment.add_obstacles(obstacles_point)

    def find_path(self, starting_point, ending_point):
        self.__path_calculator.calculate_path(starting_point, ending_point, self.__environment.get_graph())

    def print_path(self):
        logging.info(self.__path_calculator.get_calculated_path())

    def __initialize_log(self, log_level):
        if not os.path.exists(MAIN_CONTROLLER_LOG_DIR):
            os.makedirs(MAIN_CONTROLLER_LOG_DIR)
        logging.basicConfig(level=log_level, filename=MAIN_CONTROLLER_LOG_FILE, format='%(asctime)s %(message)s')
