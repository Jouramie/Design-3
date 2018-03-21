import logging
import os

from .environment_error import EnvironmentDataError
from .path_calculator.grid import Grid
from ..config import ENVIRONMENT_LOG_DIR, ENVIRONMENT_LOG_FILE


class Environment(object):
    DEFAULT_SIZE = 5
    POTENTIAL_WEIGHT = 2
    INFINITY_WEIGHT = 3
    OBSTACLE_VALUE = -2

    __width = 0
    __height = 0
    __obstacles = []
    __infrared_station = 0
    __grid = 0

    def __init__(self, log_level=logging.INFO):
        self.__initialize_log(log_level)

    def create_grid(self, width=DEFAULT_SIZE, height=DEFAULT_SIZE):
        self.__width = width
        self.__height = height
        self.__grid = Grid(self.__width, self.__height)

    def add_obstacles(self, obstacles_point):
        try:
            for point in obstacles_point:
                self.__validate_point_in_grid(point)
                self.__add_obstacle(point)
        except EnvironmentDataError as err:
            logging.info(str(err))
            return False
        return True

    def __add_obstacle(self, point):
        self.__grid.get_vertex(point).set_step_value(self.OBSTACLE_VALUE)
        for connection in self.__grid.get_vertex(point).get_connections():
            self.__grid.get_vertex(connection.get_id()).set_new_weight(
                self.__grid.get_vertex(point), self.INFINITY_WEIGHT)
            for connection_decay in self.__grid.get_vertex(connection.get_id()).get_connections():
                if not self.__grid.get_vertex(
                        connection_decay.get_id()).get_step_value() == self.OBSTACLE_VALUE and \
                        not self.__grid.get_vertex(connection.get_id()).get_step_value() == self.OBSTACLE_VALUE:
                    self.__grid.get_vertex(connection_decay.get_id()).set_new_weight(
                        self.__grid.get_vertex(connection.get_id()), self.POTENTIAL_WEIGHT)

    def __validate_point_in_grid(self, point):
        try:
            self.__grid.get_vertex(point).get_id()
        except AttributeError:
            raise EnvironmentDataError("Invalid point in environment grid: " + str(point))

    def get_grid(self):
        return self.__grid

    def __initialize_log(self, log_level):
        if not os.path.exists(ENVIRONMENT_LOG_DIR):
            os.makedirs(ENVIRONMENT_LOG_DIR)
        logging.basicConfig(level=log_level, filename=ENVIRONMENT_LOG_FILE, format='%(asctime)s %(message)s')

    def print_grid_steps(self):
        for y in range(self.__height):
            for x in range(self.__width):
                logging.info(str(self.__grid.get_vertex((x, y)).get_step_value()) + " ")
            logging.info('\n')

    def print_grid_connections(self):
        for y in range(self.__height):
            for x in range(self.__width):
                logging.info(str(self.__grid.get_vertex((x, y)).get_id()) + " Edges::")
                for connection in self.__grid.get_vertex((x, y)).get_connections():
                    logging.info(str(connection.get_id()) + " W=")
                    logging.info(str(self.__grid.get_vertex((x, y)).get_neighbor_weight(
                        self.__grid.get_vertex(connection.get_id()))) + " : ")
                logging.info('\n')
        return

    def reset_to_default(self):
        self.__grid.reset_graph()

