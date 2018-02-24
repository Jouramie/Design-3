from unittest.mock import MagicMock
from unittest import TestCase

from src.domain.environment import Environment
SOME_VALUE_0 = 0
SOME_VALUE_1 = 1
SOME_VALUE_2 = 2


class TestPathCalculator(TestCase):
    def test_when_find_path_then_call_prepare_neighbor(self):
        starting_point = (SOME_VALUE_0, SOME_VALUE_0)
        ending_point = (SOME_VALUE_1, SOME_VALUE_1)
        path_calculator = MagicMock()
        environment = Environment(path_calculator)

        environment.find_path(starting_point, ending_point)

        path_calculator.prepare_neighbor.assert_called_once_with(ending_point)

    def test_when_find_path_then_call_calculate_path(self):
        starting_point = (SOME_VALUE_0, SOME_VALUE_0)
        ending_point = (SOME_VALUE_1, SOME_VALUE_1)
        path_calculator = MagicMock()
        environment = Environment(path_calculator)

        environment.find_path(starting_point, ending_point)

        path_calculator.calculate_path.assert_called_once_with(starting_point, ending_point)

    def test_when_adding_invalid_obstacle_then_return_false(self):
        environment = Environment()
        environment.initiate_graph(SOME_VALUE_1, SOME_VALUE_1)

        value = environment.add_obstacle((SOME_VALUE_2, SOME_VALUE_2))

        self.assertFalse(value)

    def test_when_adding_obstacle_then_return_true(self):
        environment = Environment()
        environment.initiate_graph(SOME_VALUE_1, SOME_VALUE_1)

        value = environment.add_obstacle((SOME_VALUE_0, SOME_VALUE_0))

        self.assertTrue(value)
