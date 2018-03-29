from ..color import Color


class Cube(object):
    def __init__(self, center: tuple, color: Color, corners: list):
        self.center = center
        self.color = color
        self.corners = corners

    def get_colour_value(self):
        return self.color.rgb

    def get_colour_name(self):
        return self.color.name
