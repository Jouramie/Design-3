from src.domain.color import Color


class FlagCube(object):
    def __init__(self, position: tuple, color: Color):
        self.position = position
        self.color = color

    def __eq__(self, other):
        return self.position == other.position and self.color == other.color
