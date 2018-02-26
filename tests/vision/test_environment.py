import numpy as np

from unittest import TestCase
from unittest.mock import MagicMock, Mock
from vision.world_vision import *
from src.domain.environment.environment import *

cube_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-25/17h43.jpg'


class TestEnvironment(TestCase):
    def test_when_creating_environment_then_environment_is_returned(self):
        world_vision = WorldVision()
        result = world_vision.create_environment(cube_file)
        self.assertIsInstance(result[0], Environment, 'Result contains an environment object')

    def test_when_creating_environment_then_image_is_returned(self):
        world_vision = WorldVision()
        result = world_vision.create_environment(cube_file)
        self.assertIsInstance(result[1], np.ndarray, 'Result contains a ndarray image')

    def test_given_cubes_when_creating_environment_then_environment_contains_list_of_cubes(self):
        world_vision = WorldVision()
        result = world_vision.create_environment(cube_file)
        cubes_list = result[0].getCubes()
        for cube in cubes_list:
            print(cube.get_color())
            self.assertIsInstance(cube, Cube, 'Environment contains a cube')

    def test_given_obstacles_when_creating_environment_then_environment_contains_obstacles(self):
        obstacle_file = '../fig/2018-02-10/obstacles10.jpg'
