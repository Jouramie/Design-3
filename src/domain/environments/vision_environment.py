from ..objects.color import Color
from ..objects.cube import Cube
from ..objects.obstacle import Obstacle
from ..objects.target_zone import TargetZone


class VisionEnvironment(object):
    def __init__(self, cubes: [Cube], obstacles: [Obstacle], target_zone: TargetZone):
        self.cubes = cubes
        self.obstacles = obstacles
        self.target_zone = target_zone

    def find_cube(self, color: Color) -> Cube:
        # TODO déplacer dans real_world_environment
        """Return a cube matching the color in parameter

        :param color: The desired color
        :return: A cube of the desired color
        """
        for cube in self.cubes:
            if cube.color == color:
                # TODO remove cube from environments?
                return cube
        raise VisionEnvironmentError("Cube of color {} can't be found in environment.".format(color.name))

    def __str__(self):
        return "Cubes: {} \nObstacles: {} \nTarget: {}".format('', ', '.join(str(o) for o in self.obstacles),
                                                               str(self.target_zone))


class VisionEnvironmentError(Exception):
    def __init__(self, message):
        super().__init__(self, message)
