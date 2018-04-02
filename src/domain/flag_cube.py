from src.domain.color import Color


class FlagCube(object):
    def __init__(self, position: tuple, color: Color):
        self.position = position
        self.color = color
