from src.domain.objects.color import Color


class FlagCube(object):
    def __init__(self, center: tuple, color: Color):
        self.position = center
        self.color = color

    def get_3d_corners(self):
        return [(self.position[0] + 4, self.position[1] + 4, 0), (self.position[0] - 4, self.position[1] - 4, 0)]

    def __eq__(self, other):
        return self.position == other.position and self.color == other.color
