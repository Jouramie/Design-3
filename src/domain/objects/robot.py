from math import cos, sin, radians

import numpy as np


class Robot:
    def __init__(self, center: tuple, orientation: float):
        self.center = (center[0], center[1])
        self.orientation = orientation
        self.height = 22
        self.width = 22

    def get_corners(self):
        half_width = self.width / 2.0
        half_height = self.height / 2.0

        top_left = self.__get_corner(-half_width, half_height)
        top_right = self.__get_corner(half_width, half_height)
        bot_right = self.__get_corner(half_width, -half_height)
        bot_left = self.__get_corner(-half_width, -half_height)

        return np.float32([top_left, top_right, bot_right, bot_left]).reshape(-1, 3)

    def get_center_3d(self):
        return [self.center[0], self.center[1], 0]

    def __get_corner(self, offset_x, offset_y):
        orientation_rad = radians(self.orientation)
        center_x = self.center[0]
        center_y = self.center[1]
        corner_x = center_x + (offset_x * cos(orientation_rad)) - (offset_y * sin(orientation_rad))
        corner_y = center_y + (offset_x * sin(orientation_rad)) + (offset_y * cos(orientation_rad))
        corner = [corner_x, corner_y, 0]

        return corner

    def __str__(self):
        return "Position: {} cm  Orientation: {}°".format(self.center, self.orientation)
