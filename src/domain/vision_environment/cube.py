from domain.table_crop import TableCrop
from src.domain.color import Color


class Cube:
    def __init__(self, color: Color, corners: list):
        self.color = color
        self.corners = corners
        self.x = self.corners[0][0]
        self.w = self.corners[1][0]
        self.y = self.corners[0][1]
        self.h = self.corners[1][1]
        self.center = (self.x + self.w / 2, self.y + self.h / 2)

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

    def merge(self, other, table_crop: TableCrop):
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        w = max(self.w, other.w)
        h = max(self.h, other.h)
        corners = [(x + table_crop.x_crop, y + table_crop.y_crop_top),
                   (w + table_crop.x_crop, h + table_crop.y_crop_top)]
        return Cube(self.color, corners)

    def merge_center(self, other, table_crop: TableCrop):
        self_x_center = self.center[0]
        self_y_center = self.center[1]
        other_x_center = other.center[0]
        other_y_center = other.center[1]
        new_cube_x_center = round((self_x_center+other_x_center)/2)
        new_cube_y_center = round((self_y_center+other_y_center)/2)
        new_cube_x = (new_cube_x_center - 10 + table_crop.x_crop)
        new_cube_y = (new_cube_y_center - 10 + table_crop.y_crop_top)
        new_cube_w = (new_cube_x_center + 10 + table_crop.x_crop)
        new_cube_h = (new_cube_y_center + 10 + table_crop.y_crop_top)
        new_corners = [(new_cube_x, new_cube_y), (new_cube_w, new_cube_h)]
        return Cube(self.color, new_corners)


    def __eq__(self, other):
        if self.center == other.center and self.color == other.color and self.corners == other.corners:
            return True
        else:
            return False

    def __str__(self):
        return "Center: {} Color: {}".format(str(self.center), self.color.name)
