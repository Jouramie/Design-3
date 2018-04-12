from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.domain.path_calculator.path_simplifier import PathSimplifier


class TestPathSimplifier(TestCase):
    def setUp(self):
        self.navigation_environment = MagicMock()
        self.path_simplifier = PathSimplifier(self.navigation_environment, MagicMock())

    def test_given_straight_path_when_simplify_once_then_path_has_not_been_simplified(self):
        path = [(0, 0), (10, 10)]

        has_been_simplified, simplified_path = self.path_simplifier._simplify_once(path)

        self.assertFalse(has_been_simplified)
        self.assertEqual(path, simplified_path)

    def test_given_three_node_path_and_empty_environment_when_simplify_once_then_simplified_path_is_straight_line(self):
        path = [(0, 0), (10, 0), (10, 20)]
        self.navigation_environment.attach_mock(Mock(return_value=False), 'is_crossing_obstacle')

        has_been_simplified, simplified_path = self.path_simplifier._simplify_once(path)

        expected_path = [(0, 0), (10, 20)]
        self.assertEqual(expected_path, simplified_path)
        self.assertTrue(has_been_simplified)

    def test_given_path_getting_around_cube_when_simplify_once_then_do_not_change_path(self):
        path = [(0, 0), (10, 10), (20, 0)]

        def given_path_crossing_obstacle_when_is_crossing_obstacle_then_return_true(start_point, end_point):
            return start_point == (0, 0) and end_point == (20, 0)

        self.navigation_environment.attach_mock(
            Mock(side_effect=given_path_crossing_obstacle_when_is_crossing_obstacle_then_return_true),
            'is_crossing_obstacle')

        has_been_simplified, simplified_path = self.path_simplifier._simplify_once(path)

        expected_path = [(0, 0), (10, 10), (20, 0)]
        self.assertEqual(expected_path, simplified_path)
        self.assertFalse(has_been_simplified)

    def test_given_path_getting_around_cube_and_straight_line_when_simplify_once_then_remove_useless_node(self):
        path = [(0, 0), (10, 10), (20, 0), (30, 0)]

        def given_path_crossing_obstacle_when_is_crossing_obstacle_then_return_true(start_point, end_point):
            return start_point == (0, 0) and end_point == (20, 0)

        self.navigation_environment.attach_mock(
            Mock(side_effect=given_path_crossing_obstacle_when_is_crossing_obstacle_then_return_true),
            'is_crossing_obstacle')

        has_been_simplified, simplified_path = self.path_simplifier._simplify_once(path)

        expected_path = [(0, 0), (10, 10), (30, 0)]
        self.assertEqual(expected_path, simplified_path)
        self.assertTrue(has_been_simplified)

    def test_given_stair_path_getting_around_cube_when_simplify_one_then_remove_stair(self):
        path = [(0, 0), (10, 0), (10, 10), (20, 10), (20, 20)]

        def given_path_crossing_obstacle_when_is_crossing_obstacle_then_return_true(start_point, end_point):
            return start_point == (0, 0) and end_point == (20, 10) or \
                   start_point == (10, 0) and end_point == (20, 20) or \
                   start_point == (10, 0) and end_point == (20, 10)

        self.navigation_environment.attach_mock(
            Mock(side_effect=given_path_crossing_obstacle_when_is_crossing_obstacle_then_return_true),
            'is_crossing_obstacle')

        has_been_simplified, simplified_path = self.path_simplifier._simplify_once(path)

        expected_path = [(0, 0), (10, 10), (20, 20)]
        self.assertEqual(expected_path, simplified_path)
        self.assertTrue(has_been_simplified)

    def test_given_stair_path_getting_around_cube_when_simplify_then_do_straight_line(self):
        path = [(0, 0), (10, 0), (10, 10), (20, 10), (20, 20)]

        def given_path_crossing_obstacle_when_is_crossing_obstacle_then_return_true(start_point, end_point):
            return start_point == (0, 0) and end_point == (20, 10) or \
                   start_point == (10, 0) and end_point == (20, 20) or \
                   start_point == (10, 0) and end_point == (20, 10)

        self.navigation_environment.attach_mock(
            Mock(side_effect=given_path_crossing_obstacle_when_is_crossing_obstacle_then_return_true),
            'is_crossing_obstacle')

        simplified_path = self.path_simplifier.simplify(path)

        expected_path = [(0, 0), (20, 20)]
        self.assertEqual(expected_path, simplified_path)

    def test_given_stair_path_getting_around_two_cube_when_simplify_then_remove_useless_node(self):
        path = [(0, 0), (10, 0), (10, 10), (20, 10), (20, 20)]

        def given_path_crossing_obstacle_when_is_crossing_obstacle_then_return_true(start_point, end_point):
            return start_point == (0, 0) and end_point == (10, 10) or \
                   start_point == (0, 0) and end_point == (20, 10) or \
                   start_point == (0, 0) and end_point == (20, 20) or \
                   start_point == (10, 0) and end_point == (20, 20) or \
                   start_point == (10, 10) and end_point == (20, 20)

        self.navigation_environment.attach_mock(
            Mock(side_effect=given_path_crossing_obstacle_when_is_crossing_obstacle_then_return_true),
            'is_crossing_obstacle')

        simplified_path = self.path_simplifier.simplify(path)

        expected_path = [(0, 0), (10, 0), (20, 10), (20, 20)]
        self.assertEqual(expected_path, simplified_path)
