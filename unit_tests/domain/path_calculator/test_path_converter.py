from unittest import TestCase
from unittest.mock import MagicMock

from src.domain.objects.robot import Robot
from src.domain.path_calculator.direction import FORTY_FIVE_DEGREES_MOVE_LENGTH
from src.domain.path_calculator.action import Forward, Rotate
from src.domain.path_calculator.path_converter import PathConverter

FORTY_FIVE_DEGREES_MOVE_LENGTH = round(2 ** (1 / 2), 1)


class TestPathConverter(TestCase):
    def setUp(self):
        self.path_converter = PathConverter(MagicMock())
        self.robot = Robot((0, 0), 0)

    def test_when_convert_north_direction_then_command_length_is_one(self):
        path = [(0, 0), (0, 1)]

        movements, segments = self.path_converter.convert_path(path, self.robot)

        expected_movements = [Rotate(90), Forward(1)]
        expected_segments = [((0, 0), (0, 1))]
        self.assertEqual(expected_movements, movements)
        self.assertEqual(expected_segments, segments)

    def test_when_convert_south_direction_then_command_length_is_one(self):
        path = [(0, 0), (0, -1)]

        movements, segments = self.path_converter.convert_path(path, self.robot)

        expected_movements = [Rotate(-90), Forward(1)]
        expected_segments = [((0, 0), (0, -1))]
        print(', '.join(str(mouv) for mouv in movements))
        self.assertEqual(expected_movements, movements)
        self.assertEqual(expected_segments, segments)

    def test_when_convert_east_direction_then_command_length_is_one(self):
        path = [(0, 0), (1, 0)]

        movements, segments = self.path_converter.convert_path(path, self.robot)

        expected_movements = [Forward(1)]
        expected_segments = [((0, 0), (1, 0))]
        print(', '.join(str(mouv) for mouv in movements))
        self.assertEqual(expected_movements, movements)
        self.assertEqual(expected_segments, segments)

    def test_when_convert_west_direction_then_command_length_is_one(self):
        path = [(0, 0), (-1, 0)]

        movements, segments = self.path_converter.convert_path(path, self.robot)

        expected_movements = [Rotate(-180), Forward(1)]
        expected_segments = [((0, 0), (-1, 0))]
        print(', '.join(str(mouv) for mouv in movements))
        self.assertEqual(expected_movements, movements)
        self.assertEqual(expected_segments, segments)

    def test_when_convert_north_east_direction_then_command_length_is_radical_two(self):
        path = [(0, 0), (1, 1)]

        movements, segments = self.path_converter.convert_path(path, self.robot)

        expected_movements = [Rotate(45), Forward(FORTY_FIVE_DEGREES_MOVE_LENGTH)]
        expected_segments = [((0, 0), (1, 1))]
        print(', '.join(str(mouv) for mouv in movements))
        self.assertEqual(expected_movements, movements)
        self.assertEqual(expected_segments, segments)

    def test_when_convert_south_east_direction_then_command_length_is_radical_two(self):
        path = [(0, 0), (1, -1)]

        movements, segments = self.path_converter.convert_path(path, self.robot)

        expected_movements = [Rotate(-45), Forward(FORTY_FIVE_DEGREES_MOVE_LENGTH)]
        expected_segments = [((0, 0), (1, -1))]
        print(', '.join(str(mouv) for mouv in movements))
        self.assertEqual(expected_movements, movements)
        self.assertEqual(expected_segments, segments)

    def test_when_convert_north_west_direction_then_command_length_is_radical_two(self):
        path = [(0, 0), (-1, 1)]

        movements, segments = self.path_converter.convert_path(path, self.robot)

        expected_movements = [Rotate(135), Forward(FORTY_FIVE_DEGREES_MOVE_LENGTH)]
        expected_segments = [((0, 0), (-1, 1))]
        print(', '.join(str(mouv) for mouv in movements))
        self.assertEqual(expected_movements, movements)
        self.assertEqual(expected_segments, segments)

    def test_when_convert_south_west_direction_then_command_length_is_radical_two(self):
        path = [(0, 0), (-1, -1)]

        movements, segments = self.path_converter.convert_path(path, self.robot)

        expected_movements = [Rotate(-135), Forward(FORTY_FIVE_DEGREES_MOVE_LENGTH)]
        expected_segments = [((0, 0), (-1, -1))]
        print(', '.join(str(mouv) for mouv in movements))
        self.assertEqual(expected_movements, movements)
        self.assertEqual(expected_segments, segments)

    def test_when_convert_example_path_then_received_corresponding_commands(self):
        self.path = [(0, 0), (5, 5), (5, 9), (4, 9), (3, 8)]

        result_movements, result_path = self.path_converter.convert_path(self.path, self.robot, 130)

        expected_movements = [Rotate(45), Forward((round((2 * 5 ** 2) ** (1 / 2), 1))),
                              Rotate(45), Forward(4.0),
                              Rotate(90), Forward(1.0),
                              Rotate(45), Forward(FORTY_FIVE_DEGREES_MOVE_LENGTH),
                              Rotate(-95)]
        expected_path = [((0, 0), (5, 5)), ((5, 5), (5, 9)), ((5, 9), (4, 9)), ((4, 9), (3, 8))]
        self.assertEqual(expected_path, result_path)
        self.assertEqual(expected_movements, result_movements)
