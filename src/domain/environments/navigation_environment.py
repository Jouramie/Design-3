from logging import Logger

from .navigation_environment_error import NavigationEnvironmentDataError
from .real_world_environment import RealWorldEnvironment
from ..path_calculator.grid import Grid


class NavigationEnvironment(object):
    DEFAULT_HEIGHT = 231
    DEFAULT_WIDTH = 111
    POTENTIAL_WEIGHT = 2
    INFINITY_WEIGHT = 3
    OBSTACLE_VALUE = -2

    __width = 0
    __height = 0
    __obstacles = []
    __infrared_station = 0
    __grid = 0

    def __init__(self, logger: Logger):
        self.logger = logger

    def create_grid(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        self.__width = width
        self.__height = height
        self.__grid = Grid(self.__width, self.__height)

    def add_real_world_environment(self, real_world_environment: RealWorldEnvironment):

        pass  # TODO

    def add_obstacles(self, obstacles_point):
        try:
            for point in obstacles_point:
                self.__validate_point_in_grid(point)

                for x in range(-7, 7):
                    for y in range(-7, 7):
                        self.__add_obstacle((point[0] + x, point[1] + y))

        except NavigationEnvironmentDataError as err:
            self.logger.info(str(err))
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
            raise NavigationEnvironmentDataError("Invalid point in environments grid: " + str(point))

    def get_grid(self):
        return self.__grid

    def print_grid_steps(self):
        for y in range(self.__height):
            for x in range(self.__width):
                self.logger.info(str(self.__grid.get_vertex((x, y)).get_step_value()) + " ")
            self.logger.info('\n')

    def print_grid_connections(self):
        for y in range(self.__height):
            for x in range(self.__width):
                self.logger.info(str(self.__grid.get_vertex((x, y)).get_id()) + " Edges::")
                for connection in self.__grid.get_vertex((x, y)).get_connections():
                    self.logger.info(str(connection.get_id()) + " W=")
                    self.logger.info(str(self.__grid.get_vertex((x, y)).get_neighbor_weight(
                        self.__grid.get_vertex(connection.get_id()))) + " : ")
                self.logger.info('\n')
        return

    def reset_to_default(self):
        self.__grid.reset_graph()
