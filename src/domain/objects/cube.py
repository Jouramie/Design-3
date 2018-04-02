from .color import Color


class Cube(object):
    def __init__(self, center: tuple, color: Color, corners: list):
        self.center = center
        self.color = color
        self.corners = corners
