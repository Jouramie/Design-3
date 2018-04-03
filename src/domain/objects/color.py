from enum import Enum

import numpy as np


class Color(Enum):
    BLACK = ((0, 0, 0), np.array([0, 0, 0]), np.array([180, 0, 40]))
    BLUE = ((255, 0, 0), np.array([90, 40, 40]), np.array([130, 255, 255]))
    GREEN = ((0, 209, 0), np.array([40, 80, 80]), np.array([70, 255, 255]))
    RED = ((0, 0, 255), np.array([0, 80, 0]), np.array([20, 231, 200]))
    WHITE = ((255, 255, 255), np.array([30, 0, 150]), np.array([180, 255, 255]))
    YELLOW = ((0, 255, 255), np.array([26, 100, 80]), np.array([36, 255, 255]))

    SKY_BLUE = ((235, 206, 135), None, None)
    LIGHT_GREEN = ((124, 255, 124), None, None)
    LIGHT_BLUE = ((255, 124, 124), None, None)
    PINK = ((147, 20, 255), None, None)
    PINK2 = ((200, 20, 255), None, None)
    TRANSPARENT = ((230, 240, 250), None, None)

    def __init__(self, bgr: tuple, lower_bound: np.ndarray, upper_bound: np.ndarray):
        self.bgr = bgr
        self.rgb = bgr[::-1]
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    @staticmethod
    def get_from_rgb(rgb: tuple):
        for color in Color:
            if color.rgb == rgb:
                return color
