from itertools import cycle
from logging import Logger
from math import pi, atan

import numpy as np

from .action import Rotate, Forward
from ..objects.robot import Robot


class PathConverter(object):
    MAX_ITERATION = 100
    MAX_FORWARD_DISTANCE = 20  # cm

    def __init__(self, logger: Logger):
        self.logger = logger
        self.__movements = []
        self.__segments = []

    def convert_path(self, path, robot: Robot, final_angle_desired: int = None):
        self.__movements = []
        self.__segments = []

        if len(path) <= 1:
            self.__add_rotation(robot.orientation, final_angle_desired)
            return self.__movements, self.__segments

        path_cycle = cycle(path)
        iteration = 0
        current_angle = robot.orientation
        next_node = next(path_cycle)

        while iteration < self.MAX_ITERATION:
            iteration += 1

            current_node, next_node = next_node, next(path_cycle)
            movement = tuple(np.subtract(next_node, current_node))
            amplitude = round(np.linalg.norm(movement), 1)
            if movement[0] == 0:
                if movement[1] > 0:
                    new_angle = 90
                elif movement[1] < 0:
                    new_angle = -90
                else:
                    self.logger.warning('Moving of {} ?'.format(str(movement)))
                    continue
            else:
                new_angle = int(atan(movement[1] / movement[0]) / 2 / pi * 360)
                if movement[0] < 0:
                    new_angle -= 180

            self.__add_movements(amplitude, current_angle, new_angle)
            self.__add_segments(current_node, next_node)
            current_angle = new_angle
            if current_node == path[-2]:
                self.__add_rotation(current_angle, final_angle_desired)
                break

        if iteration == self.MAX_ITERATION:
            self.logger.info("PathConverter MAX_ITERATION REACH")

        return self.__movements, self.__segments

    def __add_segments(self, starting_point, ending_point):
        self.__segments.append((starting_point, ending_point))

    def __add_movements(self, length, current_angle, new_angle):
        if new_angle is not None:
            self.__add_rotation(current_angle, new_angle)
        while length >= self.MAX_FORWARD_DISTANCE:  # cm
            self.__movements.append(Forward(self.MAX_FORWARD_DISTANCE))
            length -= self.MAX_FORWARD_DISTANCE
        self.__movements.append(Forward(length))

    def __add_rotation(self, old_angle, new_angle):
        if new_angle is None:
            return
        delta_angle = new_angle - old_angle
        if (180 >= delta_angle > 0) or (-180 <= delta_angle < 0):
            self.__movements.append(Rotate(delta_angle))
        elif delta_angle % 360 == 0:
            pass
        elif delta_angle > 180:
            self.__movements.append(Rotate(delta_angle - 360))
        elif delta_angle < -180:
            self.__movements.append(Rotate(delta_angle + 360))
