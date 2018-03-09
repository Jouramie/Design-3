from unittest import TestCase
from src.vision.world_vision import *
from src.domain.environment.environment import *

cube_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-28/19h25m04s.jpg'
obstacle_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-10/obstacles10.jpg'
high_constrast_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-28/16h54m47s.jpg'
demo_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-28/19h43m00s.jpg'
no_obstacle_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-10/16h42.png'
no_cube_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-25/17h36.jpg'


class TestEnvironment(TestCase):
    def test_when_creating_environment_then_environment_is_returned(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        self.assertIsInstance(environment, Environment, 'Result contains an environment object')

    def test_when_creating_environment_then_image_is_returned(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        cv2.waitKey(0)
        self.assertIsInstance(image, np.ndarray, 'Result contains a ndarray image')

    def test_given_cubes_when_creating_environment_then_environment_contains_list_of_cubes(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        cubes_list = environment.get_cubes()
        for cube in cubes_list:
            self.assertIsInstance(cube, Cube, 'Environment contains cubes')

    def test_given_obstacles_when_creating_environment_then_environment_contains_list_of_obstacles(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        obstacles_list = environment.get_obstacles()
        cv2.imshow('result', image)
        for obstacle in obstacles_list:
            self.assertIsInstance(obstacle, Obstacle, 'Environment contains obstacles')

    def test_given_cubes_when_creating_environment_then_environment_contains_target_zone(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        target_zone = environment.get_target_zone()
        self.assertIsInstance(target_zone, TargetZone, 'Environment contains a target zone')

    def test_given_no_cube_when_creating_environment_then_environment_contains_no_cube(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(no_cube_file)
        cubes_list = environment.get_cubes()
        self.assertTrue(len(cubes_list) == 0, 'There is no cube')

    def test_given_no_obstacle_when_creating_environment_then_environment_contains_no_obstacle(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(no_obstacle_file)
        obstacles_list = environment.get_obstacles()
        self.assertTrue(len(obstacles_list) == 0, 'There is no obstacle')
