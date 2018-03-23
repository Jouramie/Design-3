from unittest import TestCase
from src.vision.world_vision import *
from domain.vision_environment.environment import *
from src.domain.color import *

cube_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-28/19h25m04s.jpg'
obstacle_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-10/obstacles10.jpg'
high_constrast_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-28/16h54m47s.jpg'
demo_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-28/19h43m00s.jpg'
no_obstacle_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-10/16h42.png'
no_cube_file = '/home/willvalin/PycharmProjects/system/fig/2018-02-25/17h36.jpg'
white_cube_file = '/home/willvalin/PycharmProjects/system/fig/2018-03-09/15h02m12s.jpg'
white_cube_file_2 = '/home/willvalin/PycharmProjects/system/fig/2018-03-09/15h01m02s.jpg'
all_cubes_file = '/home/willvalin/PycharmProjects/system/fig/2018-03-09/15h04m14s.jpg'
new_def = '/home/willvalin/PycharmProjects/system/fig/2018-03-13/20h54m23s.jpg'

class TestEnvironment(TestCase):
    def test_when_creating_environment_then_environment_is_returned(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        self.assertIsInstance(environment, Environment, 'Result contains an environment object')

    def test_when_creating_environment_then_image_is_returned(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        self.assertIsInstance(image, np.ndarray, 'Result contains a ndarray image')

    def test_given_white_cube_when_creating_environement_then_white_cube_is_returned(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(new_def)
        cubes_list = environment.get_cubes()
        cv2.imshow('White cube', image)
        cv2.waitKey(0)
        for cube in cubes_list:
            self.assertTrue(cube.get_colour_value == Color.WHITE)

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
