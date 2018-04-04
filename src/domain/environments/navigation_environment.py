from logging import Logger

from .navigation_environment_error import NavigationEnvironmentDataError
from .real_world_environment import RealWorldEnvironment
from ..objects.vision_cube import VisionCube
from ..objects.obstacle import Obstacle
from ..path_calculator.grid import Grid
from src.domain.objects.flag_cube import FlagCube


class NavigationEnvironment(object):
    DEFAULT_HEIGHT = 231
    DEFAULT_WIDTH = 111
    POTENTIAL_WEIGHT = 2
    INFINITY_WEIGHT = 3
    OBSTACLE_VALUE = -2
    CUBE_HALF_SIZE = 4
    OBSTACLE_RADIUS = 7
    # TODO Validate
    BIGGEST_ROBOT_RADIUS = 21

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
        self.add_cubes(real_world_environment.cubes)
        self.add_obstacles(real_world_environment.obstacles)
        self.__add_walls()

    def add_cubes(self, cubes: [FlagCube]):
        try:
            for cube in cubes:
                point = cube.position
                for x in range(-self.CUBE_HALF_SIZE, self.CUBE_HALF_SIZE + 1):
                    for y in range(-self.CUBE_HALF_SIZE, self.CUBE_HALF_SIZE + 1):
                        self.__set_obstacle_point(x, y, point)

        except NavigationEnvironmentDataError as err:
            self.logger.info(str(err))
            return False
        return True

    # TODO clean way to add robot dimension to obstacle, radius? orientation? position?

    def add_obstacles(self, obstacles: [Obstacle]):
        for obstacle in obstacles:
            try:
                point = (int(obstacle.center[0]), int(obstacle.center[1]))
                for x in range(-7, 8):

                    # TODO Test and chose the best shape
                    # Square seems to give path with less segment, but a little bit of space is lost on diagonal
                    # Square shape obstacle

                    for y in range(-7, 8):
                        self.__set_obstacle_point(x, y, point)

                    # Round shaped circle obstacle

            #                for y in range(-2, 3):
            #                   self.__set_obstacle_point(x, y, point)
            #          for x in range(-6, 7):
            #             for y in range(3, 5):
            #                self.__set_obstacle_point(x, y, point)
            #               self.__set_obstacle_point(-x, -y, point)
            #      for x in range(-5, 6):
            #         self.__set_obstacle_point(x, 5, point)
            #        self.__set_obstacle_point(-x, -5, point)
            #   for x in range(-4, 5):
            #      self.__set_obstacle_point(x, 6, point)
            #     self.__set_obstacle_point(-x, -6, point)
            # for x in range(-2, 3):
            #   self.__set_obstacle_point(x, 7, point)
            #  self.__set_obstacle_point(-x, -7, point)

            except NavigationEnvironmentDataError as err:
                self.logger.info(str(err))
                return False
        return True

    def __add_walls(self):
        no_go_size = self.BIGGEST_ROBOT_RADIUS + 1

        max_height = self.DEFAULT_HEIGHT + self.__grid.DEFAULT_OFFSET
        max_width = self.DEFAULT_WIDTH + self.__grid.DEFAULT_OFFSET

        for x in range(self.__grid.DEFAULT_OFFSET, max_height):
            for y in range(self.__grid.DEFAULT_OFFSET, self.__grid.DEFAULT_OFFSET + no_go_size):
                self.__add_wall(x, y)
            for y in range(max_width - no_go_size, max_width):
                self.__add_wall(x, y)

        for y in range(self.__grid.DEFAULT_OFFSET, max_width):
            for x in range(self.__grid.DEFAULT_OFFSET, self.__grid.DEFAULT_OFFSET + no_go_size):
                self.__add_wall(x, y)
            for x in range(max_height - no_go_size, max_height):
                self.__add_wall(x, y)

    def __add_wall(self, x, y):
        point = (x, y)
        self.__set_obstacle_point(0, 0, point)

    def __set_obstacle_point(self, x, y, point: tuple):
        perimeter_point = (point[0] + x, point[1] + y)
        self.__validate_point_in_grid(perimeter_point)
        self.__add_grid_obstacle(perimeter_point)

    def __add_grid_obstacle(self, point):
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
