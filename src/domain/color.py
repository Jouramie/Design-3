from enum import Enum
import numpy as np


class Color(Enum):

    BLACK = ((0, 0, 0), np.array([0, 0, 0]), np.array([180, 255, 60]))
    BLUE = ((255, 0, 0), np.array([90, 40, 40]), np.array([130, 255, 255]))
    GREEN = ((0, 255, 0), np.array([40, 80, 80]), np.array([70, 255, 255]))
    RED = ((0, 0, 255), np.array([0, 80, 0]), np.array([20, 231, 200]))
    RED2 = ((0, 0, 254), np.array([172, 80, 0]), np.array([180, 231, 200]))
    TARGET_ZONE_GREEN = ((0, 254, 0), np.array([40, 20, 40]), np.array([76, 255, 255]))
    WHITE = ((255, 255, 255), np.array([30, 0, 160]), np.array([180, 255, 255]))
    YELLOW = ((0, 255, 255), np.array([26, 100, 80]), np.array([36, 255, 255]))

    SKY_BLUE = ((235, 206, 135), None, None)
    PINK = ((147, 20, 255), None, None)

    def __init__(self, bgr: tuple, lower_bound: np.ndarray, upper_bound: np.ndarray):
        self.bgr = bgr
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
