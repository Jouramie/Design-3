from src.domain.color import Color


class Cube:
    def __init__(self, center: tuple, color: Color, corners: list):
        self.center = center
        self.color = color
        self.corners = corners

    def get_corner(self, index):
        return self.corners[index]

    def __str__(self):
        return "Center: {} Color: {}".format(str(self.center), self.color.name)
