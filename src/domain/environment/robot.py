import numpy as np

from math import cos, sin, radians


class Robot:
    def __init__(self, center: tuple, orientation: float):
        self.center = center
        self.orientation = orientation
        self.height = 16.35
        self.width = 16.35

    def get_corners(self):
        orientation_rad = radians(self.orientation)
        center_x = self.center[0]
        center_y = self.center[1]
        half_width = self.width/2.0
        half_height = self.height/2.0

        offset_top_left_x = -half_width
        offset_top_left_y = half_height
        top_left_x = center_x + (offset_top_left_x * cos(orientation_rad)) - (offset_top_left_y * sin(orientation_rad))
        top_left_y = center_y + (offset_top_left_x * sin(orientation_rad)) + (offset_top_left_y * cos(orientation_rad))
        top_left = [top_left_x, top_left_y, 0]

        offset_top_right_x = half_width
        offset_top_right_y = half_height
        top_right_x = center_x + (offset_top_right_x * cos(orientation_rad)) - (offset_top_right_y * sin(orientation_rad))
        top_right_y = center_y + (offset_top_right_x * sin(orientation_rad)) + (offset_top_right_y * cos(orientation_rad))
        top_right = [top_right_x, top_right_y, 0]

        offset_bot_right_x = half_width
        offset_bot_right_y = -half_height
        bot_right_x = center_x + (offset_bot_right_x * cos(orientation_rad)) - (offset_bot_right_y * sin(orientation_rad))
        bot_right_y = center_y + (offset_bot_right_x * sin(orientation_rad)) + (offset_bot_right_y * cos(orientation_rad))
        bot_right = [bot_right_x, bot_right_y, 0]

        offset_bot_left_x = -half_width
        offset_bot_left_y = -half_height
        bot_left_x = center_x + (offset_bot_left_x * cos(orientation_rad)) - (offset_bot_left_y * sin(orientation_rad))
        bot_left_y = center_y + (offset_bot_left_x * sin(orientation_rad)) + (offset_bot_left_y * cos(orientation_rad))
        bot_left = [bot_left_x, bot_left_y, 0]

        return np.float32([top_left, top_right, bot_right, bot_left]).reshape(-1, 3)

    def __str__(self):
        return "Position: {} cm\nOrientation : {}°".format(self.center, self.orientation)
