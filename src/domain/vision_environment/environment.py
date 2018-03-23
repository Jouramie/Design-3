from .cube import Cube
from .obstacle import Obstacle
from .target_zone import TargetZone


class Environment:
    def __init__(self, cube_list: [Cube], obstacle_list: [Obstacle], target_zone: TargetZone):
        self.__cube_list = cube_list
        self.__obstacle_list = obstacle_list
        self.__target_zone = target_zone

    def get_cubes(self) -> [Cube]:
        return self.__cube_list

    def get_obstacles(self) -> [Obstacle]:
        return self.__obstacle_list

    def get_target_zone(self) -> TargetZone:
        return self.__target_zone