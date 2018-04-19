from itertools import cycle
from logging import Logger

import numpy as np

from .action import Rotate, Forward
from ..objects.robot import Robot
from ..math_helper import get_angle


class PathConverter(object):
    MAX_ITERATION = 100
    MAX_FORWARD_DISTANCE = 50  # cm

    def __init__(self, logger: Logger):
        self.logger = logger
        self.__movements = []
        self.__segments = []

    def convert_path(self, path, robot: Robot, final_angle_desired: int = None):
        self.__movements = []
        self.__segments = []

        if len(path) <= 1:
            if final_angle_desired is not None:
                self.__movements.append(Rotate(get_rotation_angle(robot.orientation, final_angle_desired)))
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

            new_angle = get_angle(movement)

            self.__add_movements(amplitude, current_angle, new_angle)
            self.__add_segments(current_node, next_node)
            current_angle = new_angle
            if current_node == path[-2]:
                if final_angle_desired is not None:
                    self.__movements.append(Rotate(get_rotation_angle(current_angle, final_angle_desired)))
                break

        if iteration == self.MAX_ITERATION:
            self.logger.info("PathConverter MAX_ITERATION REACH")

        return self.__movements, self.__segments

    def __add_segments(self, starting_point, ending_point):
        self.__segments.append((starting_point, ending_point))

    def __add_movements(self, length, current_angle, new_angle):
        if new_angle is not None:
            rotation_angle = get_rotation_angle(current_angle, new_angle)
            if rotation_angle != 0:
                self.__movements.append(Rotate(rotation_angle))
        while length >= self.MAX_FORWARD_DISTANCE:  # cm
            self.__movements.append(Forward(self.MAX_FORWARD_DISTANCE))
            length -= self.MAX_FORWARD_DISTANCE
        self.__movements.append(Forward(length))


def get_rotation_angle(old_angle, new_angle) -> float:
    delta_angle = new_angle - old_angle
    if (180 >= delta_angle > 0) or (-180 <= delta_angle < 0):
        return delta_angle
    elif delta_angle % 360 == 0:
        return 0
    elif delta_angle > 180:
        return delta_angle - 360
    elif delta_angle < -180:
        return delta_angle + 360
