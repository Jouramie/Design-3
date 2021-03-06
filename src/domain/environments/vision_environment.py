from ..objects.obstacle import Obstacle
from ..objects.vision_cube import VisionCube


class VisionEnvironment(object):
    def __init__(self, cubes: [VisionCube], obstacles: [Obstacle]):
        self.cubes = cubes
        self.obstacles = obstacles

    def __str__(self):
        return "Cubes: {} \nObstacles: {}".format('\n    '.join(str(c) for c in self.cubes),
                                                  '\n    '.join(str(o) for o in self.obstacles))
