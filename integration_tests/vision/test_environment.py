from unittest import TestCase

from src.domain.color import *
from src.domain.vision_environment.environment import *
from src.vision.world_vision import *


demo_file = "/home/willvalin/PycharmProjects/system/fig/29-03-2018/table29-03-2018.jpg"

class TestEnvironment(TestCase):
    def test_when_creating_environment_then_environment_is_returned(self):
        world_vision = WorldVision()
        demo_frame = cv2.imread(demo_file)
        environment, image = world_vision.create_environment(demo_frame, )
        self.assertIsInstance(environment, Environment, 'Result contains an environment object')

    def test_when_creating_environment_then_image_is_returned(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file, )
        self.assertIsInstance(image, np.ndarray, 'Result contains a ndarray image')

    def test_given_white_cube_when_creating_environement_then_white_cube_is_returned(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(new_def, )
        cubes_list = environment.get_cubes()
        cv2.imshow('White cube', image)
        cv2.waitKey(0)
        for cube in cubes_list:
            self.assertTrue(cube.get_colour_value == Color.WHITE)

    def test_given_cubes_when_creating_environment_then_environment_contains_list_of_cubes(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file, )
        cubes_list = environment.get_cubes()
        for cube in cubes_list:
            self.assertIsInstance(cube, Cube, 'Environment contains cubes')

    def test_given_obstacles_when_creating_environment_then_environment_contains_list_of_obstacles(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file, )
        obstacles_list = environment.get_obstacles()
        for obstacle in obstacles_list:
            self.assertIsInstance(obstacle, Obstacle, 'Environment contains obstacles')

    def test_given_cubes_when_creating_environment_then_environment_contains_target_zone(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file, )
        target_zone = environment.get_target_zone()
        self.assertIsInstance(target_zone, TargetZone, 'Environment contains a target zone')

    def test_given_no_cube_when_creating_environment_then_environment_contains_no_cube(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(no_cube_file, )
        cubes_list = environment.get_cubes()
        self.assertTrue(len(cubes_list) == 0, 'There is no cube')

    def test_given_no_obstacle_when_creating_environment_then_environment_contains_no_obstacle(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(no_obstacle_file, )
        obstacles_list = environment.get_obstacles()
        self.assertTrue(len(obstacles_list) == 0, 'There is no obstacle')
