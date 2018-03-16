import logging
import os
import numpy

from itertools import cycle
from src.domain.path_calculator.direction import Direction
from src.config import ENVIRONMENT_LOG_DIR, ENVIRONMENT_LOG_FILE

NINETY_DEGREES_MOVE_LENGTH = 1
FORTY_FIVE_DEGREES_MOVE_LENGTH = 1.4142


class PathConverter(object):
    MAX_ITERATION = 10000
    __commands = []

    def __init__(self, log_level=logging.INFO):
        self.__initialize_log(log_level)

    def convert_path(self, path):
        self.__commands = []
        iteration = 0
        path_cycle = cycle(path)
        current_dir = 0
        current_length = 0
        next_node = next(path_cycle)

        try:
            while 1 and iteration < self.MAX_ITERATION:
                iteration += 1
                current_node, next_node = next_node, next(path_cycle)
                new_dir = tuple(numpy.subtract(next_node, current_node))
                if current_dir == 0:
                    current_dir = new_dir

                # if changing direction, add command
                # else same direction and add length
                if current_dir != new_dir:
                    self.__add_command(current_length, current_dir)
                    current_dir = new_dir
                    current_length = self.__length_to_add(current_dir)
                else:
                    current_length += self.__length_to_add(current_dir)

                # if last node, add command and break
                if current_node == path[-2]:
                    self.__add_command(current_length, current_dir)
                    break
        except Exception as err:
            logging.info(str(err))
            return 0

        if iteration == self.MAX_ITERATION:
            logging.info("PathConverter MAX_ITERATION REACH")

        return self.__commands

    def __length_to_add(self, direction):
        if Direction(direction).name in ['NORTH_EAST', 'NORTH_WEST', 'SOUTH_EAST', 'SOUTH_WEST']:
            return FORTY_FIVE_DEGREES_MOVE_LENGTH
        else:
            return NINETY_DEGREES_MOVE_LENGTH

    def __add_command(self, length, direction):
        self.__commands.append((length, Direction(direction).name))

    def __initialize_log(self, log_level):
        if not os.path.exists(ENVIRONMENT_LOG_DIR):
            os.makedirs(ENVIRONMENT_LOG_DIR)
        logging.basicConfig(level=log_level, filename=ENVIRONMENT_LOG_FILE, format='%(asctime)s %(message)s')
