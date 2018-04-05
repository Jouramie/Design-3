from enum import Enum

NINETY_DEGREES_MOVE_LENGTH = 1  # centimeters
FORTY_FIVE_DEGREES_MOVE_LENGTH = round((NINETY_DEGREES_MOVE_LENGTH * 2) ** (1 / 2), 3)


class Direction(Enum):
    SOUTH = (0, -1), 270  # degree
    NORTH = (0, 1), 90
    WEST = (-1, 0), 180
    EAST = (1, 0), 0
    SOUTH_WEST = (-1, -1), 225
    SOUTH_EAST = (1, -1), 315
    NORTH_WEST = (-1, 1), 135
    NORTH_EAST = (1, 1), 45

    def __init__(self, direction, angle):
        self.direction = direction
        self.angle = angle

    @staticmethod
    def find_direction(direction: tuple):
        if direction == (0, -1):
            return Direction.SOUTH
        elif direction == (0, 1):
            return Direction.NORTH
        elif direction == (-1, 0):
            return Direction.WEST
        elif direction == (1, 0):
            return Direction.EAST
        elif direction == (-1, -1):
            return Direction.SOUTH_WEST
        elif direction == (1, -1):
            return Direction.SOUTH_EAST
        elif direction == (-1, 1):
            return Direction.NORTH_WEST
        elif direction == (1, 1):
            return Direction.NORTH_EAST
        else:
            raise ValueError("Direction doest not exist")

    def length_to_add(self):
        if self.angle % 90 == 0:
            return NINETY_DEGREES_MOVE_LENGTH
        else:
            return FORTY_FIVE_DEGREES_MOVE_LENGTH
