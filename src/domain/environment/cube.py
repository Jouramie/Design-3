class Cube:
    def __init__(self, center, color):
        self.center = center
        self.color = color

    def get_color(self):
        return self.color

    def get_x_position(self):
        return self.center[0]

    def get_y_position(self):
        return self.center[1]
