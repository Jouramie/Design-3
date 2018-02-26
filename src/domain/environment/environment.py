from src.domain.environment.cube import *
from src.domain.environment.obstacle import *
from src.domain.environment.target_zone import *


class Environment:
    def __init__(self, cube_list: [Cube], obstacle_list: [Obstacle], target_zone,):
        self.cube_list = cube_list
        self.target_zone = target_zone
        self.obstacle_list = obstacle_list

    def getCubes(self):
        return self.cube_list