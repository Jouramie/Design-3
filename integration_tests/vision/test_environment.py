from unittest import TestCase

from src.domain.objects.color import *
from src.vision.world_vision import *




class TestEnvironment(TestCase):
    def test_when_creating_environment_then_environment_is_returned(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        self.assertIsInstance(environment, VisionEnvironment, 'Result contains an environments object')

    def test_when_creating_environment_then_image_is_returned(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        self.assertIsInstance(image, np.ndarray, 'Result contains a ndarray image')

    def test_given_white_cube_when_creating_environment_then_white_cube_is_returned(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(new_def)
        cubes_list = environment.cubes
        cv2.imshow('White cube', image)
        cv2.waitKey(0)
        for cube in cubes_list:
            self.assertTrue(cube.color == Color.WHITE)

    def test_given_cubes_when_creating_environment_then_environment_contains_list_of_cubes(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        cubes_list = environment.cubes
        for cube in cubes_list:
            self.assertIsInstance(cube, Cube, 'Environment contains cubes')

    def test_given_obstacles_when_creating_environment_then_environment_contains_list_of_obstacles(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        obstacles_list = environment.obstacles
        for obstacle in obstacles_list:
            self.assertIsInstance(obstacle, Obstacle, 'Environment contains obstacles')

    def test_given_cubes_when_creating_environment_then_environment_contains_target_zone(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(demo_file)
        target_zone = environment.target_zone
        self.assertIsInstance(target_zone, TargetZone, 'Environment contains a target zone')

    def test_given_no_cube_when_creating_environment_then_environment_contains_no_cube(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(no_cube_file)
        cubes_list = environment.cubes
        self.assertTrue(len(cubes_list) == 0, 'There is no cube')

    def test_given_no_obstacle_when_creating_environment_then_environment_contains_no_obstacle(self):
        world_vision = WorldVision()
        environment, image = world_vision.create_environment(no_obstacle_file)
        obstacles_list = environment.obstacles
        self.assertTrue(len(obstacles_list) == 0, 'There is no obstacle')
