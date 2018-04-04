from .color import Color


class Cube(object):
    def __init__(self, center: tuple, color: Color, corners: list):
        self.center = center
        self.color = color
        self.corners = corners

    def get_3d_corners(self) -> [tuple]:
        return list(map(self.__to_3d, self.corners))

    def __to_3d(self, corner: tuple) -> tuple:
        return corner[0], corner[1], 0

    def __str__(self) -> str:
        return "Center: {}, Color: {}, Corners: {}".format(str(self.center), self.color.name, str(self.corners))
