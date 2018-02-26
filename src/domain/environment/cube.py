class Cube:
    def __init__(self, color, center):
        self.color = color
        self.center = center

    def get_color(self):
        return self.color.value

    def get_x_position(self):
        return self.center.getX()

    def get_y_position(self):
        return self.center.getY()
