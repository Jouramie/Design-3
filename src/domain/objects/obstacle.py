class Obstacle:
    def __init__(self, center: tuple, radius: float):
        self.center = center
        self.radius = radius

    def __str__(self) -> str:
        return "Center: {}, Radius: {}".format(str(self.center), str(self.radius))
