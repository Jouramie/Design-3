from domain.vision_environment.cube import Cube
from .obstacle import Obstacle
from .target_zone import TargetZone
from ..color import Color


class VisionEnvironment:
    def __init__(self, cubes: [Cube], obstacles: [Obstacle], target_zone: TargetZone):
        self.cubes = cubes
        self.obstacles = obstacles
        self.target_zone = target_zone

    def find_cube(self, color: Color) -> Cube:
        """Return a cube matching the color in parameter

        :param color: The desired color
        :return: A cube of the desired color
        """
        for cube in self.cubes:
            if cube.color == color:
                # TODO remove cube from environment?
                return cube

    def __str__(self):
        return "Cubes: {} \nObstacles: {} \nTarget: {}".format(str(self.cubes), str(self.obstacles),
                                                               str(self.target_zone))
