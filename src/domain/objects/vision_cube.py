from src.vision.table_crop import TableCrop
from .color import Color


class VisionCube(object):
    def __init__(self, color: Color, corners: list):
        self.color = color
        self.corners = corners
        self.x = self.corners[0][0]
        self.w = self.corners[1][0]
        self.y = self.corners[0][1]
        self.h = self.corners[1][1]
        self.center = ((self.x + self.w) / 2, (self.y + self.h) / 2)

    def get_center(self):
        return self.center

    def get_corner(self, index):
        return self.corners[index]

    def set_color(self, color: Color):
        self.color = color

    def get_area(self):
        area = (self.x + self.w)*(self.y + self.h)
        return area

    def get_horizontal_middle(self):
        return (self.x + self.w)/2

    def get_vertical_middle(self):
        return (self.y + self.h)/2

    def get_color(self):
        return self.color

    def set_color(self, new_color):
        self.color = new_color

    def get_x_adjusted(self):
        return self.x + TableCrop.x_crop

    def get_y_adjusted(self):
        return self.y + TableCrop.y_crop

    def get_w_adjusted(self):
        return self.w + TableCrop.w_crop

    def get_h_adjusted(self):
        return self.h + TableCrop.h_crop

    def is_inside(self, other):
        if other.x >= self.x and other.y >= self.y and other.w >= self.w and other.h >= self.h:
            return True
        else:
            return False

    def is_too_close(self, other):
        vertical_distance = 70
        horizontal_distance = 30
        if (abs(self.get_horizontal_middle() - other.get_horizontal_middle()) <= 20) and \
                (abs(self.get_vertical_middle() - other.get_vertical_middle()) <= vertical_distance):
            return True
        if (abs(self.x - other.w) <= horizontal_distance or abs(self.x - other.x) <= horizontal_distance or
            abs(self.w - other.w) <= horizontal_distance) and (abs(self.y - other.y) <= vertical_distance):
            return True
        else:
            return False

    def __eq__(self, other):
        if self.center == other.center and self.color == other.color and self.corners == other.corners:
            return True
        else:
            return False

    def __str__(self) -> str:
        return "Center: {} Color: {}".format(str(self.center), self.color.name)
