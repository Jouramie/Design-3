from itertools import cycle
from src.domain.path_calculator.direction import Direction

import numpy


class PathConverter(object):
    def convert_path(self, path):
        path_cycle = cycle(path)

        current_dir = 0
        current_length = 0
        commands = []

        next_node = next(path_cycle)

        while 1:
            current_node, next_node = next_node, next(path_cycle)

            new_dir = tuple(numpy.subtract(next_node, current_node))

            #print(current_node, end=" next: ")
            #print(next_node)

            # Set initial direction
            if current_dir == 0:
                current_dir = new_dir

            # If changing direction, add commands
            # else same direction, add length
            if current_dir != new_dir:
                commands.append((current_length, Direction(current_dir).name))
                current_dir = new_dir
                current_length = 1
            else:
                current_length += 1

            print(current_length, end=" towards: ")
            print(current_dir)
            # If last node, add command
            if current_node == path[-2]:
                commands.append((current_length, Direction(current_dir).name))
                break

        print(commands)


# [(1,1),(2,2),(3,3),(4,4),(5,5),(5,6),(5,7),(5,8),(5,9),(4,9),(3,9)]