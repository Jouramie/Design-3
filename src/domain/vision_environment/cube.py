from src.domain.color import Color


class Cube:
    def __init__(self, center: tuple, color: Color, corners: list):
        self.center = center
        self.color = color
        self.corners = corners
        self.x = self.corners[0][0]
        self.w = self.corners[1][0]
        self.y = self.corners[0][1]
        self.h = self.corners[1][1]

    def get_corner(self, index):
        return self.corners[index]

    def set_color(self, color: Color):
        self.color = color

    def get_horizontal_middle(self):
        return (self.x + self.w)/2

    def get_y(self):
        y = self.corners[0][1]
        return y

    def get_h(self):
        h = self.corners[1][1]
        return h

    def get_vertical_middle(self):
        return (self.y + self.h)/2

    def get_color(self):
        return self.color

    def __str__(self):
        return "Center: {} Color: {}".format(str(self.center), self.color.name)

