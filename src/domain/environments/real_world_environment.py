from src.domain.objects.wall import Wall
from ..objects.color import Color
from ..objects.flag_cube import FlagCube
from ..objects.obstacle import Obstacle
from ..objects.target_zone import TargetZone

from math import sqrt


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

    def find_cube(self, color: Color, safe_area: tuple) -> FlagCube:
        matching_color_cubes = []
        shortest_distance_between_cube_center_and_safe_area = 200
        closest_cube = None
        for cube in self.cubes:
            if cube.color == color:
                matching_color_cubes.append(cube)

        for cube in matching_color_cubes:
            if cube.wall == Wall.MIDDLE:
                distance_between_robot_and_cube = sqrt((safe_area[1] - cube.center[1]) ** 2
                                                       + (safe_area[0] - cube.center[0]) ** 2)
                if distance_between_robot_and_cube < shortest_distance_between_cube_center_and_safe_area:
                    shortest_distance_between_cube_center_and_safe_area = distance_between_robot_and_cube
                    closest_cube = cube

        if closest_cube is not None:
            return closest_cube

        if len(matching_color_cubes) != 0:
            return matching_color_cubes[0]
        else:
            return None

