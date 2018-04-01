from unittest import TestCase

from src.domain.navigation_environment import NavigationEnvironment

SOME_INVALID_VALUE = -10000
SOME_VALUE_0 = 0
SOME_VALUE_1 = 1
SOME_VALUE_2 = 2


class TestNavigationEnvironment(TestCase):
    def test_when_adding_invalid_obstacle_then_return_false(self):
        environment = NavigationEnvironment()
        environment.create_grid()

        value = environment.add_obstacles([(SOME_INVALID_VALUE, SOME_INVALID_VALUE)])

        self.assertFalse(value)

    def test_when_adding_obstacle_then_return_true(self):
        environment = NavigationEnvironment()
        environment.create_grid()

        value = environment.add_obstacles([(SOME_VALUE_0, SOME_VALUE_0)])

        self.assertTrue(value)
