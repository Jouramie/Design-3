from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import Mock

from src.domain.environments.navigation_environment import NavigationEnvironment
from src.domain.objects.obstacle import Obstacle
from src.domain.path_calculator.path_calculator import PathCalculator
from src.domain.path_calculator.path_calculator_error import PathCalculatorError, PathCalculatorNoPathError

SOME_VALUE_0 = 0
SOME_VALUE_1 = 1
SOME_VALUE_2 = 2
END_POINT_VALUE = 0
UNASSIGNED_VALUE = -1


class TestPathCalculator(TestCase):
    def test_when_calculate_path_with_invalid_grid_then_exception_raised(self):
        starting_point = (SOME_VALUE_1, SOME_VALUE_1)
        ending_point = (SOME_VALUE_2, SOME_VALUE_2)
        invalid_grid = 0
        path_calculator = PathCalculator()

        with self.assertRaises(PathCalculatorError):
            path_calculator.calculate_path(starting_point, ending_point, invalid_grid)

    def test_when_calculate_path_with_invalid_starting_point_then_exception_raised(self):
        starting_point = (SOME_VALUE_2, SOME_VALUE_1)
        starting_vertex = MagicMock()
        starting_vertex.attach_mock(Mock(return_value=UNASSIGNED_VALUE), 'get_step_value')
        ending_point = (SOME_VALUE_2, SOME_VALUE_1)
        grid = Mock()
        path_calculator = PathCalculator()
        grid.attach_mock(Mock(return_value=starting_vertex), 'get_vertex')

        with self.assertRaises(PathCalculatorNoPathError):
            path_calculator.calculate_path(starting_point, ending_point, grid)

    def test_when_calculate_path_then_validate_path_exist(self):
        starting_point = (SOME_VALUE_2, SOME_VALUE_1)
        starting_vertex = MagicMock()
        ending_point = (SOME_VALUE_2, SOME_VALUE_1)
        grid = Mock()
        path_calculator = PathCalculator()
        grid.attach_mock(Mock(return_value=starting_vertex), 'get_vertex')

        path_calculator.calculate_path(starting_point, ending_point, grid)

        starting_vertex.get_step_value.assert_called_once()

    def test_when_calculate_path_then_set_ending_point_step_value(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        starting_point = (SOME_VALUE_0, SOME_VALUE_0)
        ending_point = (SOME_VALUE_1, SOME_VALUE_0)
        path_calculator = PathCalculator()

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = environment.get_grid().get_vertex(ending_point).get_step_value() + 1

        self.assertEqual(expected, environment.get_grid().get_vertex(starting_point).get_step_value())

    def test_when_calculate_path_then_increment_neighbor_step_value(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        starting_point = (SOME_VALUE_0, SOME_VALUE_0)
        ending_point = (SOME_VALUE_1, SOME_VALUE_0)
        path_calculator = PathCalculator()

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = END_POINT_VALUE

        self.assertEqual(expected, environment.get_grid().get_vertex(ending_point).get_step_value())

    def test_when_calculate_path_then_calculate_path(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        starting_point = (SOME_VALUE_1, SOME_VALUE_0)
        ending_point = (SOME_VALUE_0, SOME_VALUE_0)
        path_calculator = PathCalculator()

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = [starting_point, ending_point]

        self.assertEqual(expected, path_calculator.get_calculated_path())

    def test_when_straight_line_then_does_not_zigzag(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        starting_point = (0, 0)
        ending_point = (10, 0)
        path_calculator = PathCalculator()

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0)]

        self.assertEqual(expected, path_calculator.get_calculated_path())

    def test_when_diagonal_line_then_does_not_zigzag(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        starting_point = (0, 0)
        ending_point = (10, 10)
        path_calculator = PathCalculator()

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)]

        self.assertEqual(expected, path_calculator.get_calculated_path())

    def test_when_obstacle_then_goes_around_it(self):
        environment = NavigationEnvironment(MagicMock())
        environment.create_grid()
        environment.add_obstacles([Obstacle((0, 0), 7)])
        starting_point_next_to_obstacle = (-8, 1)
        ending_point_next_to_obstacle = (8, 0)
        path_calculator = PathCalculator()

        path_calculator.calculate_path(starting_point_next_to_obstacle, ending_point_next_to_obstacle,
                                       environment.get_grid())
        expected = [(-8, 1), (-9, 2), (-9, 3), (-8, 4), (-8, 5), (-7, 6), (-6, 7), (-5, 8), (-4, 8), (-3, 9), (-2, 9),
                    (-1, 9), (0, 9), (1, 9), (2, 9), (3, 9), (4, 8), (5, 8), (6, 7), (7, 6), (8, 5), (8, 4), (9, 3),
                    (9, 2), (9, 1), (9, 0), (9, -1), (8, 0)]

        expected_square = [(-8, 1), (-9, 2), (-9, 3), (-9, 4), (-9, 5), (-9, 6), (-9, 7), (-9, 8), (-8, 9), (-7, 9),
                         (-6, 9), (-5, 9), (-4, 9), (-3, 9), (-2, 9), (-1, 9), (0, 9), (1, 9), (2, 9), (3, 9), (4, 9),
                         (5, 9), (6, 9), (7, 9), (8, 9), (9, 8), (9, 7), (9, 6), (9, 5), (9, 4), (9, 3), (9, 2), (9, 1),
                         (9, 0), (9, -1), (8, 0)]

        self.assertEqual(expected_square, path_calculator.get_calculated_path())
