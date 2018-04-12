from unittest import TestCase
from unittest.mock import MagicMock

from src.domain.environments.navigation_environment import NavigationEnvironment
from src.domain.environments.navigation_environment_error import NavigationEnvironmentDataError
from src.domain.environments.real_world_environment import RealWorldEnvironment
from src.domain.objects.flag_cube import FlagCube
from src.domain.objects.obstacle import Obstacle
from src.domain.path_calculator.grid import Grid

SOME_INVALID_VALUE = -10000
OBSTACLE_POSITION = (30, 30)
INVALID_OBSTACLE_POSITION = (-1000, -1000)
CUBE_POSITION = (30, 30)
SOME_VALUE_0 = 0
SOME_VALUE_1 = 1
SOME_VALUE_2 = 2


class TestNavigationEnvironment(TestCase):
    def test_given_no_size_when_create_grid_create_correct_grid_size(self):
        navigation_environment = NavigationEnvironment(MagicMock())
        navigation_environment.create_grid()

        expected_number_of_vertex = (NavigationEnvironment.DEFAULT_WIDTH + 1) * (NavigationEnvironment.DEFAULT_HEIGHT + 1)

        self.assertEqual(expected_number_of_vertex, len(navigation_environment.get_grid().get_vertices()))

    def test_given_obstacle_when_adding_obstacles_then_add_obstacle_to_navigation_environment(self):
        obstacle = Obstacle(OBSTACLE_POSITION, NavigationEnvironment.OBSTACLE_RADIUS)
        obs_list = []
        obs_list.append(obstacle)

        navigation_environment = NavigationEnvironment(MagicMock())
        navigation_environment.create_grid()
        navigation_environment.add_obstacles(obs_list)

        for x in range(OBSTACLE_POSITION[0] - NavigationEnvironment.OBSTACLE_RADIUS + Grid.DEFAULT_OFFSET,
                       OBSTACLE_POSITION[0] + NavigationEnvironment.OBSTACLE_RADIUS + 1):
            for y in range(OBSTACLE_POSITION[1] - NavigationEnvironment.OBSTACLE_RADIUS + Grid.DEFAULT_OFFSET,
                           OBSTACLE_POSITION[1] + NavigationEnvironment.OBSTACLE_RADIUS + 1):
                self.assertEqual(Grid.OBSTACLE_VALUE,
                                 navigation_environment.get_grid().get_vertex((x, y)).get_step_value())

    def test_when_adding_cubes_then_add_obstacle_to_navigation_environment(self):
        cube = FlagCube(CUBE_POSITION, MagicMock())
        cube_list = []
        cube_list.append(cube)

        navigation_environment = NavigationEnvironment(MagicMock())
        navigation_environment.create_grid()
        navigation_environment.add_cubes(cube_list)

        for x in range(CUBE_POSITION[0] - NavigationEnvironment.CUBE_HALF_SIZE + Grid.DEFAULT_OFFSET,
                       CUBE_POSITION[0] + NavigationEnvironment.CUBE_HALF_SIZE + 1):
            for y in range(CUBE_POSITION[1] - NavigationEnvironment.CUBE_HALF_SIZE + Grid.DEFAULT_OFFSET,
                           CUBE_POSITION[1] + NavigationEnvironment.CUBE_HALF_SIZE + 1):
                self.assertEqual(Grid.OBSTACLE_VALUE,
                                 navigation_environment.get_grid().get_vertex((x, y)).get_step_value())

    def test_when_add_real_world_environment_then_add_walls_to_navigation_environment(self):
        obs_list = []
        cube_list = []
        real_world_environment = RealWorldEnvironment(MagicMock(), MagicMock())
        real_world_environment.obstacles = obs_list
        real_world_environment.cubes = cube_list
        navigation_environment = NavigationEnvironment(MagicMock())
        navigation_environment.create_grid()
        navigation_environment.add_real_world_environment(real_world_environment)

        max_height = NavigationEnvironment.DEFAULT_HEIGHT + Grid.DEFAULT_OFFSET
        max_width = NavigationEnvironment.DEFAULT_WIDTH + Grid.DEFAULT_OFFSET

        # Validate all 4 walls are correctly represented
        for x in range(Grid.DEFAULT_OFFSET, max_height):
            for y in range(Grid.DEFAULT_OFFSET, Grid.DEFAULT_OFFSET + navigation_environment.BIGGEST_ROBOT_RADIUS + 1):
                self.assertEqual(Grid.OBSTACLE_VALUE,
                                 navigation_environment.get_grid().get_vertex((x, y)).get_step_value())
            for y in range(max_width - navigation_environment.BIGGEST_ROBOT_RADIUS, max_width):
                self.assertEqual(Grid.OBSTACLE_VALUE,
                                 navigation_environment.get_grid().get_vertex((x, y)).get_step_value())
        for y in range(Grid.DEFAULT_OFFSET, max_width):
            for x in range(Grid.DEFAULT_OFFSET, Grid.DEFAULT_OFFSET + navigation_environment.BIGGEST_ROBOT_RADIUS + 1):
                self.assertEqual(Grid.OBSTACLE_VALUE,
                                 navigation_environment.get_grid().get_vertex((x, y)).get_step_value())
            for x in range(max_height - navigation_environment.BIGGEST_ROBOT_RADIUS, max_height):
                self.assertEqual(Grid.OBSTACLE_VALUE,
                                 navigation_environment.get_grid().get_vertex((x, y)).get_step_value())

    def test_given_invalid_obstacle_then_exception_raised(self):
        obstacle = Obstacle(INVALID_OBSTACLE_POSITION, NavigationEnvironment.OBSTACLE_RADIUS)
        obs_list = []
        obs_list.append(obstacle)

        navigation_environment = NavigationEnvironment(MagicMock())
        navigation_environment.create_grid()

        self.assertRaises(NavigationEnvironmentDataError, navigation_environment.add_obstacles(obs_list))
