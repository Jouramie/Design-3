from itertools import cycle
from logging import Logger

import numpy

from .direction import Direction
from .movement import Rotate, Forward
from ..objects.robot import Robot

MAX_ITERATION = 10000


class PathConverter(object):

    def __init__(self, logger: Logger):
        self.logger = logger
        self.__movements = []
        self.__segments = []

    def convert_path(self, path, robot: Robot, final_direction_desired: Direction = None):
        self.__movements = []
        self.__segments = []
        path_cycle = cycle(path)

        iteration = 0
        current_length = 0

        starting_point = None
        current_direction: Direction = None

        next_node = next(path_cycle)

        if len(path) <= 1:
            self.__add_rotation(robot.orientation, final_direction_desired.angle)
            return self.__movements, self.__segments

        while iteration < MAX_ITERATION:
            iteration += 1

            current_node, next_node = next_node, next(path_cycle)
            new_dir = tuple(numpy.subtract(next_node, current_node))
            new_direction = Direction.find_direction(new_dir)

            if current_direction is None:
                if robot.orientation != new_direction.angle:
                    self.__add_rotation(robot.orientation, new_direction.angle)
                current_direction = new_direction
                starting_point = current_node

            if current_direction == new_direction:
                current_length += current_direction.length_to_add()
            else:
                self.__add_movements(current_length, current_direction, new_direction)
                self.__add_segments(starting_point, current_node)
                current_direction = new_direction
                starting_point = current_node
                current_length = current_direction.length_to_add()

            if current_node == path[-2]:
                self.__add_movements(current_length, current_direction, final_direction_desired)
                self.__add_segments(starting_point, next_node)
                break

        if iteration == MAX_ITERATION:
            self.logger.info("PathConverter MAX_ITERATION REACH")

        return self.__movements, self.__segments

    def __add_segments(self, starting_point, ending_point):
        self.__segments.append((starting_point, ending_point))

    def __add_movements(self, length, current_direction, new_direction):
        self.__movements.append(Forward(length))
        if new_direction is not None:
            self.__add_rotation(current_direction.angle, new_direction.angle)

    def __add_rotation(self, old_angle, new_angle):
        delta_angle = new_angle - old_angle
        if (180 >= delta_angle > 0) or (-180 <= delta_angle < 0):
            self.__movements.append(Rotate(delta_angle))
        elif delta_angle == 0:
            pass
        elif delta_angle > 180:
            self.__movements.append(Rotate(delta_angle - 360))
        elif delta_angle < -180:
            self.__movements.append(Rotate(delta_angle + 360))
