import logging
import os
import numpy

from itertools import cycle
from .direction import Direction
from .path_calculator_error import PathConverterError
from src.config import PATH_CONVERTER_LOG_DIR, PATH_CONVERTER_LOG_FILE


class PathConverter(object):
    MAX_ITERATION = 10000
    __commands = []
    __path = []

    def __init__(self, log_level=logging.INFO):
        self.__initialize_log(log_level)

    def convert_path(self, path):
        self.__path = path
        self.__commands = []
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

                if current_dir != new_dir:
                    self.__add_command(current_length, current_dir)
                    current_dir = new_dir
                    current_length = Direction.length_to_add(self.__find_direction_name(current_dir))
                else:
                    current_length += Direction.length_to_add(self.__find_direction_name(current_dir))

                if current_node == self.__path[-2]:
                    self.__add_command(current_length, current_dir)
                    break
        except PathConverterError as err:
            logging.info(str(err))
            return 0

        if iteration == self.MAX_ITERATION:
            logging.info("PathConverter MAX_ITERATION REACH")

        return self.__commands

    def __add_command(self, length, direction):
        self.__commands.append((length, self.__find_direction_name(direction)))

    def __find_direction_name(self, direction):
        try:
            return Direction(direction).name
        except ValueError:
            raise PathConverterError("Invalid direction %s, in path %s" % (str(direction), str(self.__path)))

    def __initialize_log(self, log_level):
        if not os.path.exists(PATH_CONVERTER_LOG_DIR):
            os.makedirs(PATH_CONVERTER_LOG_DIR)
        logging.basicConfig(level=log_level, filename=PATH_CONVERTER_LOG_FILE, format='%(asctime)s %(message)s')
