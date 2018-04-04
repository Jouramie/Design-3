from src.vision.coordinate_converter import CoordinateConverter
from .vision_environment import VisionEnvironment
from ..objects.color import Color
from ..objects.vision_cube import VisionCube
from ..objects.flag_cube import FlagCube
import scipy
from scipy import spatial
import numpy as np

class RealWorldEnvironment(object):
    def __init__(self, vision_environment: VisionEnvironment,
                 coordinate_converter: CoordinateConverter, cube_dictionnary: dict):
        self.obstacles = coordinate_converter.project_obstacles(vision_environment.obstacles)
        self.table_config_cubes = cube_dictionnary
        self.cubes = self.convert_vision_cubes_to_real_world_environment_cubes(vision_environment.cubes)
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

    def convert_vision_cubes_to_real_world_environment_cubes(self, vision_cubes) -> [FlagCube]:
        real_cubes = []
        cube_pixel_positions_x_list = []
        cube_pixel_positions_y_list = []
        for table_cube in self.table_config_cubes.values():
            pixel_x = table_cube['pixel_x']
            pixel_y = table_cube['pixel_y']
            cube_pixel_positions_x_list.append(pixel_x)
            cube_pixel_positions_y_list.append(pixel_y)
        pixel_x_nparray = np.asarray(cube_pixel_positions_x_list)
        pixel_y_nparray = np.asarray(cube_pixel_positions_y_list)
        combined_x_y_arrays = np.dstack([pixel_x_nparray.ravel(), pixel_y_nparray.ravel()])[0]
        tree = spatial.cKDTree(combined_x_y_arrays)
        for vision_cube in vision_cubes:
            dist, indexes = tree.query(vision_cube.get_center())
            table_cube = self.table_config_cubes['cube' + str(indexes)]
            position = (table_cube['x'], table_cube['y'])
            color = vision_cube.get_color()
            flag_cube = FlagCube(position, color)
            real_cubes.append(flag_cube)

        return real_cubes


