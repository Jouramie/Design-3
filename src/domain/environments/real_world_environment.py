from src.domain.objects.wall import Wall
from ..objects.color import Color
from ..objects.flag_cube import FlagCube
from ..objects.obstacle import Obstacle
from ..objects.target_zone import TargetZone


class RealWorldEnvironment(object):
    def __init__(self, obstacles: [Obstacle] = None, cubes: [FlagCube] = None, target_zone: TargetZone = None):
        self.obstacles = obstacles
        if self.obstacles is None:
            self.obstacles = []
        self.cubes = cubes
        if self.cubes is None:
            self.cubes = []
        self.target_zone = target_zone

    def __str__(self):
        return "Cubes: {} \nObstacles: {} \nTarget: {}".format('\n    '.join(str(c) for c in self.cubes),
                                                               '\n    '.join(str(o) for o in self.obstacles),
                                                               str(self.target_zone))

    def find_cube(self, color: Color) -> FlagCube:
        """Return a cube matching the color in parameter

        :param color: The desired color
        :return: A cube of the desired color
        """
        matching_color_cubes = []
        for cube in self.cubes:
            if cube.color == color:
                matching_color_cubes.append(cube)

        for cube in matching_color_cubes:
            if cube.wall == Wall.MIDDLE:
                return cube

        if matching_color_cubes.count() != 0:
            return matching_color_cubes[0]
        else:
            return None

