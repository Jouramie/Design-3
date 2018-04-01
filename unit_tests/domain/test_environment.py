from unittest import TestCase

from src.domain.navigation_environment import NavigationEnvironment
SOME_NEGATIVE_VALUE = -1
SOME_VALUE_0 = 0
SOME_VALUE_1 = 1
SOME_VALUE_2 = 2


class TestPathCalculator(TestCase):
    def test_when_adding_invalid_obstacle_then_return_false(self):
        environment = NavigationEnvironment()
        environment.create_grid()

        value = environment.add_obstacles([(SOME_NEGATIVE_VALUE, SOME_NEGATIVE_VALUE)])

        self.assertFalse(value)

    def test_when_adding_obstacle_then_return_true(self):
        environment = NavigationEnvironment()
        environment.create_grid()

        value = environment.add_obstacles([(SOME_VALUE_0, SOME_VALUE_0)])

        self.assertTrue(value)
