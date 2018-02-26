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
        cv2.imshow('Result', result[1])
        cv2.waitKey(0)

    def test_given_cubes_when_creating_environment_then_environment_contains_list_of_cubes(self):
        world_vision = WorldVision()
        result = world_vision.create_environment(cube_file)
        cubes_list = result[0].get_cubes()
        for cube in cubes_list:
            self.assertIsInstance(cube, Cube, 'Environment contains cubes')

    def test_given_cubes_when_creating_environment_then_environment_contains_list_of_obstacles(self):
        world_vision = WorldVision()
        result = world_vision.create_environment(cube_file)
        obstacles_list = result[0].get_obstacles()
        for obstacle in obstacles_list:
            self.assertIsInstance(obstacle, Obstacle, 'Environment contains obstacles')

    def test_given_cubes_when_creating_environment_then_environment_contains_target_zone(self):
        world_vision = WorldVision()
        result = world_vision.create_environment(cube_file)
        target_zone = result[0].get_target_zone()
        self.assertIsInstance(target_zone, TargetZone, 'Environment contains a target zone')
