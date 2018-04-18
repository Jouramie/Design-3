import numpy as np

from math import atan, pi
from typing import Union


def distance_between(point1: tuple, point2: tuple) -> float:
    vector = np.subtract(point2, point1)
    return round(np.linalg.norm(vector), 3)


def get_normalized_direction(start_point: tuple, destination_point: tuple) -> np.ndarray:
    vector = np.subtract(destination_point, start_point)
    return normalize(vector)


def normalize(vector: np.ndarray) -> np.ndarray:
    return vector / np.linalg.norm(vector)


def get_angle(vector: Union[tuple, np.ndarray]) -> float:
    if vector[0] == 0:
        if vector[1] > 0:
            return 90
        elif vector[1] < 0:
            return -90
        else:
            return 0

    angle = float(atan(vector[1] / vector[0]) / 2 / pi * 360)
    if vector[0] < 0:
        angle -= 180
    return angle



