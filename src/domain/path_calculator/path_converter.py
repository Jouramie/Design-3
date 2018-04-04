from itertools import cycle
from logging import Logger

import numpy

from .direction import Direction
from .path_calculator_error import PathConverterError


class PathConverter(object):
    MAX_ITERATION = 10000
    __commands = []
    __segments = []
    __path = []

    def __init__(self, logger: Logger):
        self.logger = logger

    def convert_path(self, path):
        self.__path = path
        self.__commands = []
        self.__segments = []
        starting_point = ()
        iteration = 0
        path_cycle = cycle(self.__path)
        current_dir = None
        current_length = 0
        next_node = next(path_cycle)

        try:
            while True and iteration < self.MAX_ITERATION:
                iteration += 1
                current_node, next_node = next_node, next(path_cycle)
                new_dir = tuple(numpy.subtract(next_node, current_node))
                if current_dir is None:
                    current_dir = new_dir
                    starting_point = current_node

                if current_dir != new_dir:
                    self.__add_command(current_length, current_dir)
                    self.__add_segments(starting_point, current_node)
                    current_dir = new_dir
                    starting_point = current_node
                    current_length = Direction.length_to_add(self.__find_direction_name(current_dir))
                else:
                    current_length += Direction.length_to_add(self.__find_direction_name(current_dir))

                if current_node == self.__path[-2]:
                    self.__add_command(current_length, current_dir)
                    self.__add_segments(starting_point, next_node)
                    break
        except PathConverterError as err:
            self.logger.info(str(err))

        if iteration == self.MAX_ITERATION:
            self.logger.info("PathConverter MAX_ITERATION REACH")

        return self.__commands, self.__segments

    def __add_segments(self, starting_point, ending_point):
        self.__segments.append((starting_point, ending_point))

    def __add_command(self, length, direction):
        self.__commands.append((length, self.__find_direction_name(direction)))

    def __find_direction_name(self, direction):
        try:
            return Direction(direction).name
        except ValueError:
            raise PathConverterError("Invalid direction %s, in path %s" % (str(direction), str(self.__path)))
