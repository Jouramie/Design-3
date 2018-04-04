from src.domain.objects.flag_cube import FlagCube
from src.vision.coordinate_converter import CoordinateConverter
from .vision_environment import VisionEnvironment
from ..objects.color import Color
from ..objects.vision_cube import VisionCube
import scipy
import numpy as np

class RealWorldEnvironment(object):
    def __init__(self, vision_environment: VisionEnvironment,
                 coordinate_converter: CoordinateConverter, cube_dictionnary: dict):
        # TODO déplacer dans une factory
        self.obstacles = coordinate_converter.project_obstacles(vision_environment.obstacles)
        self.table_config_cubes = cube_dictionnary
        self.cubes = self.convert_vision_cubes_to_real_world_environment_cubes(vision_environment.cubes)
        self.target_zone = None


    def __str__(self):
        return "Cubes: {} \nObstacles: {} \nTarget: {}".format('\n    '.join(str(c) for c in self.cubes),
                                                               '\n    '.join(str(o) for o in self.obstacles),
                                                               str(self.target_zone))

    def find_cube(self, color: Color) -> VisionCube:
        """Return a cube matching the color in parameter

        :param color: The desired color
        :return: A cube of the desired color
        """
        for cube in self.cubes:
            if cube.color == color:
                # TODO remove cube from environments?
                return cube
        return None  # TODO raise une exception

    def convert_vision_cubes_to_real_world_environment_cubes(self, vision_cubes) -> FlagCube:
        real_cubes = []
        cube_pixel_positions_x_list = []
        cube_pixel_positions_y_list = []
        for table_cube in self.table_config_cubes.values():
            x = table_cube['pixel_x']
            y = table_cube['pixel_y']
            cube_pixel_positions_x_list.append(x)
            cube_pixel_positions_y_list.append(y)
        a = np.asarray(cube_pixel_positions_x_list)
        b = np.asarray(cube_pixel_positions_y_list)
        combined_x_y_arrays = np.dstack([a.ravel(), b.ravel()])[0]
        tree = scipy.spatial.cKDTree(combined_x_y_arrays)
        for vision_cube in vision_cubes:
            dist, indexes = tree.query(vision_cube.get_center())
            print(indexes)


        #Check which cube is closest


