from logging import Logger

from src.domain.objects.flag_cube import FlagCube
from .navigation_environment_error import NavigationEnvironmentDataError
from .real_world_environment import RealWorldEnvironment
from ..objects.obstacle import Obstacle
from ..path_calculator.grid import Grid
from ..path_calculator.path_calculator import PathCalculator


class NavigationEnvironment(object):
    DEFAULT_HEIGHT = 231
    DEFAULT_WIDTH = 111
    POTENTIAL_WEIGHT = 2
    INFINITY_WEIGHT = 3
    CUBE_HALF_SIZE = 4
    OBSTACLE_RADIUS = 7
    BIGGEST_ROBOT_RADIUS = 23

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
        for cube in cubes:
            point = cube.center
            for x in range(-self.CUBE_HALF_SIZE - self.BIGGEST_ROBOT_RADIUS, self.CUBE_HALF_SIZE +
                                                                             self.BIGGEST_ROBOT_RADIUS + 1):
                for y in range(-self.CUBE_HALF_SIZE - self.BIGGEST_ROBOT_RADIUS, self.CUBE_HALF_SIZE +
                                                                                 self.BIGGEST_ROBOT_RADIUS + 1):
                    try:
                        self.__set_obstacle_point(x, y, point)
                    except NavigationEnvironmentDataError as err:
                        self.logger.info(str(err))
                        pass

    def add_obstacles(self, obstacles: [Obstacle]):
        for obstacle in obstacles:
            point = (int(obstacle.center[0]), int(obstacle.center[1]))
            print(point)
            for x in range(-self.OBSTACLE_RADIUS - self.BIGGEST_ROBOT_RADIUS, self.OBSTACLE_RADIUS +
                                                                              self.BIGGEST_ROBOT_RADIUS + 1):
                # Square shape obstacle
                for y in range(-self.OBSTACLE_RADIUS - self.BIGGEST_ROBOT_RADIUS, self.OBSTACLE_RADIUS +
                                                                                  self.BIGGEST_ROBOT_RADIUS + 1):
                    try:
                        self.__set_obstacle_point(x, y, point)
                    except NavigationEnvironmentDataError as err:
                        self.logger.info(str(err))
                        pass

    def __add_walls(self):
        max_height = self.DEFAULT_HEIGHT + self.__grid.DEFAULT_OFFSET
        max_width = self.DEFAULT_WIDTH + self.__grid.DEFAULT_OFFSET

        for x in range(self.__grid.DEFAULT_OFFSET, max_height):
            for y in range(self.__grid.DEFAULT_OFFSET, self.__grid.DEFAULT_OFFSET + self.BIGGEST_ROBOT_RADIUS + 1):
                self.__add_wall(x, y)
            for y in range(max_width - self.BIGGEST_ROBOT_RADIUS, max_width):
                self.__add_wall(x, y)

        for y in range(self.__grid.DEFAULT_OFFSET, max_width):
            for x in range(self.__grid.DEFAULT_OFFSET, self.__grid.DEFAULT_OFFSET + self.BIGGEST_ROBOT_RADIUS + 1):
                self.__add_wall(x, y)
            for x in range(max_height - self.BIGGEST_ROBOT_RADIUS, max_height):
                self.__add_wall(x, y)

    def __add_wall(self, x, y):
        point = (x, y)
        self.__set_obstacle_point(0, 0, point)

    def __set_obstacle_point(self, x, y, point: tuple):
        perimeter_point = (point[0] + x, point[1] + y)
        self.__validate_point_in_grid(perimeter_point)
        self.__add_grid_obstacle(perimeter_point)

    def __add_grid_obstacle(self, point):
        self.__grid.get_vertex(point).set_step_value(PathCalculator.OBSTACLE_VALUE)
        for connection in self.__grid.get_vertex(point).get_connections():
            self.__grid.get_vertex(connection.get_id()).set_new_weight(
                self.__grid.get_vertex(point), self.INFINITY_WEIGHT)

    def __validate_point_in_grid(self, point):
        try:
            self.__grid.get_vertex(point).get_id()
        except AttributeError:
            raise NavigationEnvironmentDataError("Invalid point in environments grid: " + str(point))

    def get_grid(self):
        return self.__grid
