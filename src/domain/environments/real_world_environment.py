from src.vision.coordinate_converter import CoordinateConverter
from .vision_environment import VisionEnvironment
from ..objects.color import Color
from ..objects.vision_cube import VisionCube
from ..objects.flag_cube import FlagCube
from scipy import spatial
import numpy as np

class RealWorldEnvironment(object):
    def __init__(self, vision_environment: VisionEnvironment,
                 coordinate_converter: CoordinateConverter):
        self.obstacles = coordinate_converter.project_obstacles(vision_environment.obstacles)
        self.cubes = coordinate_converter.convert_vision_cubes_to_real_world_environment_cubes(vision_environment.cubes)
        self.target_zone = None

    def __str__(self):
        return "Cubes: {} \nObstacles: {} \nTarget: {}".format('\n    '.join(str(c) for c in self.cubes),
                                                               '\n    '.join(str(o) for o in self.obstacles),
                                                               str(self.target_zone))

    def find_cube(self, color: Color) -> FlagCube:
        """Return a cube matching the color in parameter

        :param color: The desired color
        :return: A cube of the desired color
        """
        for cube in self.cubes:
            if cube.color == color:
                return cube
        return None


