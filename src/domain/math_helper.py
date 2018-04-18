import numpy as np


def distance_between(point1: tuple, point2: tuple) -> float:
    movement = tuple(np.subtract(point2, point1))
    return round(np.linalg.norm(movement), 3)
