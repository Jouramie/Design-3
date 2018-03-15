from itertools import cycle
from src.domain.path_calculator.direction import Direction

import numpy


class PathConverter(object):
    MAX_ITERATION = 10000

    __commands = []

    def convert_path(self, path):
        iteration = 0
        path_cycle = cycle(path)
        current_dir = 0
        current_length = 0
        next_node = next(path_cycle)

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

        print(self.__commands)

    def __length_to_add(self, direction):
        if Direction(direction).name in ['NORTH_EAST', 'NORTH_WEST', 'SOUTH_EAST', 'SOUTH_WEST']:
            return 1.4142
        else:
            return 1

    def __add_command(self, length, direction):
        self.__commands.append((length, Direction(direction).name))

# [(1,1),(2,2),(3,3),(4,4),(5,5),(5,6),(5,7),(5,8),(5,9),(4,9),(3,9)]