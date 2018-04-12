from enum import Enum


class TableCrop(Enum):
    TABLE1 = (0, 210, 210)
    TABLE2 = (30, 230, 230)
    TABLE3 = (24, 210, 210)
    TABLE4 = (12, 230, 230)
    TABLE5 = (12, 228, 224)
    TABLE6 = (12, 228, 224)

    def __init__(self, x_crop, y_crop_top, y_crop_bot):
        self.x_crop = x_crop
        self.y_crop_top = y_crop_top
        self.y_crop_bot = y_crop_bot
