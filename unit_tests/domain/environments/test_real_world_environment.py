from unittest import TestCase

from src.domain.environments.real_world_environment import RealWorldEnvironment
from src.domain.objects.color import Color
from src.domain.objects.flag_cube import FlagCube
from src.domain.objects.obstacle import Obstacle
from src.domain.objects.robot import Robot
from src.domain.objects.wall import Wall

CUBE_LIST = [FlagCube((166.5, 84.5), Color.GREEN, Wall.UP), FlagCube((180.5, 84.5), Color.GREEN, Wall.UP),
             FlagCube((203.5, 60.5), Color.BLUE, Wall.MIDDLE), FlagCube((203.5, 46.5), Color.GREEN, Wall.MIDDLE),
             FlagCube((203.5, 32.5), Color.BLUE, Wall.MIDDLE), FlagCube((203.5, 18.5), Color.BLACK, Wall.MIDDLE),
             FlagCube((203.5, 4.5), Color.YELLOW, Wall.MIDDLE), FlagCube((180.5, -19.5), Color.RED, Wall.DOWN),
             FlagCube((166.5, -19.5), Color.BLUE, Wall.DOWN)]

SAFE_AREA = (166, 33)
EXPECTED_MIDDLE_CUBE = FlagCube((203.5, 32.5), Color.BLUE, Wall.MIDDLE)
EXPECTED_DOWN_CUBE = FlagCube((180.5, -19.5), Color.RED, Wall.DOWN)

OBSTACLE_RADIUS = 7
ROBOT_DIRECTION = 0
ANY_ROBOT = Robot((0, 0), ROBOT_DIRECTION)


class TestRealWorldEnvironment(TestCase):
    def test_given_safe_area_and_color_from_middle_when_get_next_cube_should_return_closest_cube(self):
        real_world_environment = RealWorldEnvironment(None, CUBE_LIST, None)
        next_cube = real_world_environment.find_cube(Color.BLUE, SAFE_AREA)

        self.assertEqual(EXPECTED_MIDDLE_CUBE, next_cube)

    def test_given_safe_area_and_color_not_from_middle_when_get_next_cube_should_return_up_or_down_cube(self):
        real_world_environment = RealWorldEnvironment(None, CUBE_LIST, None)
        next_cube = real_world_environment.find_cube(Color.RED, SAFE_AREA)

        self.assertEqual(EXPECTED_DOWN_CUBE, next_cube)

    def test_given_safe_area_and_not_available_color_when_get_next_cube_should_return_none(self):
        real_world_environment = RealWorldEnvironment(None, CUBE_LIST, None)
        next_cube = real_world_environment.find_cube(Color.WHITE, SAFE_AREA)

        self.assertEqual(None, next_cube)

    def test_given_no_obstacles_when_find_two_closest_obstacles_then_return_empty_list(self):
        real_world_environment = RealWorldEnvironment()

        self.assertFalse(real_world_environment.find_two_closest_obstacles(ANY_ROBOT))

    def test_given_two_obstacles_when_find_two_closest_obstacles_then_return_obstacles(self):
        obstacles = [Obstacle((10, 10), OBSTACLE_RADIUS), Obstacle((20, 20), OBSTACLE_RADIUS)]
        real_world_environment = RealWorldEnvironment(obstacles=obstacles)

        self.assertEqual(obstacles, real_world_environment.find_two_closest_obstacles(ANY_ROBOT))

    def test_given_three_obstacles_when_find_two_closest_obstacles_then_return_two_closest_obstacles(self):
        expected_closest_obstacles = [Obstacle((10, 10), OBSTACLE_RADIUS), Obstacle((20, 10), OBSTACLE_RADIUS)]
        obstacles = list(expected_closest_obstacles)
        obstacles.append(Obstacle((100, 100), OBSTACLE_RADIUS))
        robot = Robot((15, 10), ROBOT_DIRECTION)
        real_world_environment = RealWorldEnvironment(obstacles=obstacles)

        closest_obstacles = real_world_environment.find_two_closest_obstacles(robot)

        self.assertEqual(expected_closest_obstacles, closest_obstacles)
