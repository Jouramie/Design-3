from src.domain.objects.color import Color


class FlagCube(object):
    def __init__(self, center: tuple, color: Color):
        self.center = center
        self.color = color

    def get_3d_corners(self):
        return [(self.center[0] + 4, self.center[1] + 4, 0), (self.center[0] - 4, self.center[1] - 4, 0)]

    def __str__(self):
        return "Position: {}, Color: {}".format(self.center, self.color)

    def __eq__(self, other):
        return self.center == other.center and self.color == other.color
