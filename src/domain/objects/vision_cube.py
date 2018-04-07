from src.vision.table_crop import TableCrop
from .color import Color


class VisionCube(object):
    def __init__(self, color: Color, corners: list):
        self.color = color
        self.corners = corners
        x = self.corners[0][0]
        w = self.corners[1][0]
        y = self.corners[0][1]
        h = self.corners[1][1]
        self.center = ((x + w) / 2, (y + h) / 2)

    def __str__(self) -> str:
        return "Center: {} Color: {}".format(str(self.center), self.color.name)
