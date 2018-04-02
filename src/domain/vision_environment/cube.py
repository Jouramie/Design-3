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

    def get_vertical_middle(self):
        return (self.y + self.h)/2

    def get_color(self):
        return self.color

    def is_inside(self, other):
        if self.x >= other.x and self.y >= other.y and self.w <= other.w and self.h <= other.h:
            return True
        else:
            return False

    def is_too_close(self, other):
        if abs(self.get_horizontal_middle() - other.get_horizontal_middle()) <= 20:
            return True
        else:
            return False

    def __eq__(self, other):
        if self.center == other.center and self.color == other.color and self.corners == other.corners:
            return True
        else:
            return False

    def __str__(self):
        return "Center: {} Color: {}".format(str(self.center), self.color.name)

