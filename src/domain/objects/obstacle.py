class Obstacle:
    def __init__(self, center: tuple, radius: float):
        self.center = center
        self.radius = radius

    def get_radius_line(self):
        return [self.center, (self.center[0] + self.radius, self.center[1])]

    def __str__(self) -> str:
        return "Center: {}, Radius: {}".format(str(self.center), str(self.radius))
