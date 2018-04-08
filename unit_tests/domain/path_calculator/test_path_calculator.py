from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import Mock

from src.domain.environments.navigation_environment import NavigationEnvironment
from src.domain.objects.obstacle import Obstacle
from src.domain.path_calculator.path_calculator import PathCalculator
from src.domain.path_calculator.path_calculator_error import PathCalculatorError, PathCalculatorNoPathError
from src.domain.path_calculator.grid import Grid

SPECIFIC_OBSTACLE_1_VALUE = (104, 0)
SPECIFIC_OBSTACLE_2_VALUE = (42, 62)
SPECIFIC_STARTING_POINT = (50, 15)
SPECIFIC_ENDING_POINT = (102, 33)

SOME_VALUE_0 = 0
SOME_VALUE_1 = 1
SOME_VALUE_2 = 2
SOME_OBSTACLE_LOCATION = 50
END_POINT_VALUE = 0
UNASSIGNED_VALUE = -1


class TestPathCalculator(TestCase):
    def test_when_calculate_path_then_validate_path_exist(self):
        starting_point = (SOME_VALUE_2, SOME_VALUE_1)
        starting_vertex = MagicMock()
        ending_point = (SOME_VALUE_2, SOME_VALUE_1)
        grid = Mock()
        path_calculator = PathCalculator(MagicMock())
        grid.attach_mock(Mock(return_value=starting_vertex), 'get_vertex')

        path_calculator.calculate_path(starting_point, ending_point, grid)

        self.assertEquals(2, starting_vertex.get_step_value.call_count)

    def test_when_calculate_path_then_set_ending_point_step_value(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        starting_point = (SOME_VALUE_0, SOME_VALUE_0)
        ending_point = (SOME_VALUE_1, SOME_VALUE_0)
        path_calculator = PathCalculator(MagicMock())

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = environment.get_grid().get_vertex(ending_point).get_step_value() + 1

        self.assertEqual(expected, environment.get_grid().get_vertex(starting_point).get_step_value())

    def test_when_calculate_path_then_increment_neighbor_step_value(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        starting_point = (SOME_VALUE_0, SOME_VALUE_0)
        ending_point = (SOME_VALUE_1, SOME_VALUE_0)
        path_calculator = PathCalculator(MagicMock())

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = END_POINT_VALUE

        self.assertEqual(expected, environment.get_grid().get_vertex(ending_point).get_step_value())

    def test_when_calculate_path_then_calculate_path(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        starting_point = (SOME_VALUE_1, SOME_VALUE_0)
        ending_point = (SOME_VALUE_0, SOME_VALUE_0)
        path_calculator = PathCalculator(MagicMock())

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = [starting_point, ending_point]

        self.assertEqual(expected, path_calculator.get_calculated_path())

    def test_when_calculating_then_recommend_forward(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        environment.add_obstacles([Obstacle(SPECIFIC_OBSTACLE_1_VALUE, NavigationEnvironment.OBSTACLE_RADIUS),
                                   Obstacle(SPECIFIC_OBSTACLE_2_VALUE, NavigationEnvironment.OBSTACLE_RADIUS)])

        starting_point = SPECIFIC_STARTING_POINT
        ending_point = SPECIFIC_ENDING_POINT

        path_calculator = PathCalculator(MagicMock())

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())

        expected_square = [(50, 15), (50, 16), (50, 17), (50, 18), (50, 19), (50, 20), (50, 21), (50, 22), (50, 23),
                           (50, 24), (50, 25), (50, 26), (50, 27), (50, 28), (50, 29), (50, 30), (50, 31), (51, 31),
                           (52, 31), (53, 31), (54, 31), (55, 31), (56, 31), (57, 31), (58, 31), (59, 31), (60, 31),
                           (61, 31), (62, 31), (63, 31), (64, 31), (65, 31), (66, 31), (67, 31), (68, 31), (69, 31),
                           (70, 31), (71, 31), (72, 31), (73, 31), (74, 31), (75, 31), (76, 31), (77, 31), (78, 31),
                           (79, 31), (80, 31), (81, 31), (82, 31), (83, 31), (84, 31), (85, 31), (86, 31), (87, 31),
                           (88, 31), (89, 31), (90, 31), (91, 31), (92, 31), (93, 31), (94, 31), (95, 31), (96, 31),
                           (97, 31), (98, 31), (99, 31), (100, 31), (101, 31), (102, 31), (102, 32), (102, 33)]

        self.assertEqual(expected_square, path_calculator.get_calculated_path())

    def test_when_straight_line_then_does_not_zigzag(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        starting_point = (0, 0)
        ending_point = (10, 0)
        path_calculator = PathCalculator(MagicMock())

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0)]

        self.assertEqual(expected, path_calculator.get_calculated_path())

    def test_when_diagonal_line_then_does_a_triangle(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        starting_point = (0, 0)
        ending_point = (10, 10)
        path_calculator = PathCalculator(MagicMock())

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (1, 10),
                    (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10)]

        self.assertEqual(expected, path_calculator.get_calculated_path())

    def test_when_obstacle_then_goes_around_it(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        environment.add_obstacles([Obstacle((SOME_OBSTACLE_LOCATION, SOME_OBSTACLE_LOCATION),
                                            NavigationEnvironment.OBSTACLE_RADIUS)])

        starting_point_next_to_obstacle = (SOME_OBSTACLE_LOCATION + Grid.DEFAULT_OFFSET -
                                           NavigationEnvironment.OBSTACLE_RADIUS - 1, SOME_OBSTACLE_LOCATION + 1)
        ending_point_next_to_obstacle = (SOME_OBSTACLE_LOCATION - Grid.DEFAULT_OFFSET +
                                         NavigationEnvironment.OBSTACLE_RADIUS, SOME_OBSTACLE_LOCATION)
        path_calculator = PathCalculator(MagicMock())

        path_calculator.calculate_path(starting_point_next_to_obstacle, ending_point_next_to_obstacle,
                                       environment.get_grid())

        expected = [(19, 51), (19, 52), (19, 53), (19, 54), (19, 55), (19, 56), (19, 57), (19, 58), (19, 59), (19, 60),
         (19, 61), (19, 62), (19, 63), (19, 64), (19, 65), (19, 66), (19, 67), (19, 68), (19, 69), (19, 70),
         (19, 71), (19, 72), (19, 73), (19, 74), (19, 75), (19, 76), (19, 77), (19, 78), (19, 79), (19, 80),
         (19, 81), (20, 81), (21, 81), (22, 81), (23, 81), (24, 81), (25, 81), (26, 81), (27, 81), (28, 81),
         (29, 81), (30, 81), (31, 81), (32, 81), (33, 81), (34, 81), (35, 81), (36, 81), (37, 81), (38, 81),
         (39, 81), (40, 81), (41, 81), (42, 81), (43, 81), (44, 81), (45, 81), (46, 81), (47, 81), (48, 81),
         (49, 81), (50, 81), (51, 81), (52, 81), (53, 81), (54, 81), (55, 81), (56, 81), (57, 81), (58, 81),
         (59, 81), (60, 81), (61, 81), (62, 81), (63, 81), (64, 81), (65, 81), (66, 81), (67, 81), (68, 81),
         (69, 81), (70, 81), (71, 81), (72, 81), (73, 81), (74, 81), (75, 81), (76, 81), (77, 81), (78, 81),
         (79, 81), (80, 81), (81, 81), (81, 80), (81, 79), (81, 78), (81, 77), (81, 76), (81, 75), (81, 74),
         (81, 73), (81, 72), (81, 71), (81, 70), (81, 69), (81, 68), (81, 67), (81, 66), (81, 65), (81, 64),
         (81, 63), (81, 62), (81, 61), (81, 60), (81, 59), (81, 58), (81, 57), (81, 56), (81, 55), (81, 54),
         (81, 53), (81, 52), (81, 51), (81, 50)]

        self.assertEqual(expected, path_calculator.get_calculated_path())
