import numpy as np

from unittest import TestCase
from unittest.mock import MagicMock, Mock
from vision.world_vision import *
from src.domain.environment.environment import *

cube_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-25/17h43.jpg'
obstacle_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-10/obstacles10.jpg'
no_obstacle_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-10/16h42.png'


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

    def test_given_no_cube_when_creating_environment_then_environment_contains_no_cube(self):
        world_vision = WorldVision()
        result = world_vision.create_environment(obstacle_file)
        cubes_list = result[0].get_cubes()
        self.assertTrue(len(cubes_list) == 0, 'There is no cube')

    def test_given_no_obstacle_when_creating_environment_then_environment_contains_no_obstacle(self):
        world_vision = WorldVision()
        result = world_vision.create_environment(no_obstacle_file)
        obstacles_list = result[0].get_obstacles()
        cv2.imshow('result', result[1])
        cv2.waitKey(0)
        self.assertTrue(len(obstacles_list) == 0, 'There is no obstacle')
