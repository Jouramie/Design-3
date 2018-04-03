from ..objects.cube import Cube
from ..objects.obstacle import Obstacle
from ..objects.target_zone import TargetZone


class VisionEnvironment(object):
    def __init__(self, cubes: [Cube], obstacles: [Obstacle], target_zone: TargetZone):
        self.cubes = cubes
        self.obstacles = obstacles
        self.target_zone = target_zone

    def __str__(self):
        return "Cubes: {} \nObstacles: {} \nTarget: {}".format('\n    '.join(str(c) for c in self.cubes),
                                                               '\n    '.join(str(o) for o in self.obstacles),
                                                               str(self.target_zone))
