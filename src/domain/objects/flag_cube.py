from src.domain.objects.color import Color
from src.domain.objects.wall import Wall


class FlagCube(object):
    def __init__(self, center: tuple, color: Color, wall: Wall = None):
        self.center = center
        self.color = color
        self.is_placed = False
        self.wall = wall

    def get_corners(self):
        return [(self.center[0] + 4, self.center[1] + 4), (self.center[0] - 4, self.center[1] - 4)]

    def place_cube(self):
        self.is_placed = True

    def __str__(self):
        return "Position: {}, Color: {}".format(self.center, self.color)

    def __eq__(self, other):
        return self.center == other.center and self.color == other.color and self.wall == other.wall
