from logging import Logger

from src.domain.environments.navigation_environment import NavigationEnvironment
from src.domain.path_calculator.path_calculator import PathCalculator


class MainController(object):
    __environment = 0
    __path_calculator = 0

    def __init__(self, logger: Logger):
        self.logger = logger
        self.__environment = NavigationEnvironment(logger)
        self.__path_calculator = PathCalculator()

    def create_environment(self, obstacles_point):
        # call world_vision.create_environment()
        # find some way to feed size from point to graph
        self.__environment.create_grid()
        self.__environment.add_obstacles(obstacles_point)

    def find_path(self, starting_point, ending_point):
        self.__path_calculator.calculate_path(starting_point, ending_point, self.__environment.get_grid())

    def print_path(self):
        self.logger.info(self.__path_calculator.get_calculated_path())
