from enum import Enum


class Direction(Enum):
    NORTH = (0, -1)
    SOUTH = (0, 1)
    EAST = (-1, 0)
    WEST = (1, 0)
    NORTH_EAST = (-1, -1)
    NORTH_WEST = (1, -1)
    SOUTH_EAST = (-1, 1)
    SOUTH_WEST = (1, 1)
    NINETY_DEGREES_MOVE_LENGTH = 1
    FORTY_FIVE_DEGREES_MOVE_LENGTH = round((NINETY_DEGREES_MOVE_LENGTH*2)**(1/2), 3)

    @staticmethod
    def length_to_add(direction):
        if direction in [Direction.NORTH_EAST.name, Direction.NORTH_WEST.name,
                         Direction.SOUTH_EAST.name, Direction.SOUTH_WEST.name]:
            return Direction.FORTY_FIVE_DEGREES_MOVE_LENGTH.value
        else:
            return Direction.NINETY_DEGREES_MOVE_LENGTH.value
