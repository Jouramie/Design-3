from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest import TestCase
import csv

from src.domain.environment import Environment
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
        environment = Environment()
        environment.create_grid(SOME_VALUE_2, SOME_VALUE_1)
        starting_point = (SOME_VALUE_0, SOME_VALUE_0)
        ending_point = (SOME_VALUE_1, SOME_VALUE_0)
        path_calculator = PathCalculator()

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = environment.get_grid().get_vertex(ending_point).get_step_value() + 1

        self.assertEqual(expected, environment.get_grid().get_vertex(starting_point).get_step_value())

    def test_when_calculate_path_then_increment_neighbor_step_value(self):
        environment = Environment()
        environment.create_grid(SOME_VALUE_2, SOME_VALUE_1)
        starting_point = (SOME_VALUE_0, SOME_VALUE_0)
        ending_point = (SOME_VALUE_1, SOME_VALUE_0)
        path_calculator = PathCalculator()

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = END_POINT_VALUE

        self.assertEqual(expected, environment.get_grid().get_vertex(ending_point).get_step_value())

    def test_when_calculate_path_then_calculate_path(self):
        environment = Environment()
        environment.create_grid(SOME_VALUE_2, SOME_VALUE_1)
        starting_point = (SOME_VALUE_1, SOME_VALUE_0)
        ending_point = (SOME_VALUE_0, SOME_VALUE_0)
        path_calculator = PathCalculator()

        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())
        expected = [starting_point, ending_point]
        
        self.assertEqual(expected, path_calculator.get_calculated_path())

    def test_demonstration_that_create_csv(self):
        environment = Environment()
        environment.create_grid(6, 6)
        obstacles = [(2, 2), (2, 3), (3, 2), (3, 3)]
        #obstacles = [(2, 1), (3, 1), (4, 1), (5, 1), (1, 5), (2, 5), (3, 5)]
        environment.add_obstacles(obstacles)
        starting_point = (0, 0)
        ending_point = (5, 5)
        path_calculator = PathCalculator()
        path_calculator.calculate_path(starting_point, ending_point, environment.get_grid())

        my_file = open("path_demo.csv", "w")
        try:
            with my_file:
                my_data = ""
                for y in range(6):
                    for x in range(6):
                        my_data += str(environment.get_grid().get_vertex((x, y)).get_step_value()) + ","
                    my_data += '\n'
                my_file.write(my_data)
        except FileNotFoundError:
            print("not found")

        my_file = open("path_demo.csv", "a")
        try:
            with my_file:
                my_data = ""
                for y in range(6):
                    for x in range(6):
                        if (x, y) in path_calculator.get_calculated_path():
                            my_data += "X" + ","
                        else:
                            my_data += "_" + ","
                    my_data += '\n'
                my_file.write(my_data)
        except FileNotFoundError:
            print("not found")
