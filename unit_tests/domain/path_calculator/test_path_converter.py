from unittest import TestCase
from unittest.mock import MagicMock

from src.domain.objects.robot import Robot
from src.domain.path_calculator.direction import Direction
from src.domain.path_calculator.direction import FORTY_FIVE_DEGREES_MOVE_LENGTH
from src.domain.path_calculator.direction import NINETY_DEGREES_MOVE_LENGTH
from src.domain.path_calculator.action import Forward, Rotate
from src.domain.path_calculator.path_converter import PathConverter


class TestPathConverter(TestCase):
    def setUp(self):
        self.path_converter = PathConverter(MagicMock())
        self.path = []
        self.path.append((0, 0))
        self.robot = Robot((0, 0), 0)

    def test_when_convert_north_direction_then_command_length_is_one(self):
        self.path.append(Direction.NORTH.direction)

        expected = [Rotate(90), Forward(NINETY_DEGREES_MOVE_LENGTH)], [((0, 0), (0, 1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path, self.robot))

    def test_when_convert_south_direction_then_command_length_is_one(self):
        self.path.append(Direction.SOUTH.direction)

        expected = [Rotate(-90), Forward(NINETY_DEGREES_MOVE_LENGTH)], [((0, 0), (0, -1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path, self.robot))

    def test_when_convert_east_direction_then_command_length_is_one(self):
        self.path.append(Direction.EAST.direction)

        expected = [Forward(NINETY_DEGREES_MOVE_LENGTH)], [((0, 0), (1, 0))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path, self.robot))

    def test_when_convert_west_direction_then_command_length_is_one(self):
        self.path.append(Direction.WEST.direction)

        expected = [Rotate(180), Forward(NINETY_DEGREES_MOVE_LENGTH)], [((0, 0), (-1, 0))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path, self.robot))

    def test_when_convert_north_east_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.NORTH_EAST.direction)

        expected = [Rotate(45), Forward(FORTY_FIVE_DEGREES_MOVE_LENGTH)], [((0, 0), (1, 1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path, self.robot))

    def test_when_convert_south_east_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.SOUTH_EAST.direction)

        expected = [Rotate(-45), Forward(FORTY_FIVE_DEGREES_MOVE_LENGTH)], [((0, 0), (1, -1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path, self.robot))

    def test_when_convert_north_west_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.NORTH_WEST.direction)

        expected = [Rotate(135), Forward(FORTY_FIVE_DEGREES_MOVE_LENGTH)], [((0, 0), (-1, 1))]

        result = self.path_converter.convert_path(self.path, self.robot)
        self.assertEqual(expected, result)

    def test_when_convert_south_west_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.SOUTH_WEST.direction)

        expected = [Rotate(-135), Forward(FORTY_FIVE_DEGREES_MOVE_LENGTH)], [((0, 0), (-1, -1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path, self.robot))

    def test_when_convert_example_path_then_received_corresponding_commands(self):
        self.path = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (4, 9), (3, 8)]
        expected_movements = [Rotate(45), Forward(5 * FORTY_FIVE_DEGREES_MOVE_LENGTH),
                              Rotate(45), Forward(4 * NINETY_DEGREES_MOVE_LENGTH),
                              Rotate(90), Forward(NINETY_DEGREES_MOVE_LENGTH),
                              Rotate(45), Forward(FORTY_FIVE_DEGREES_MOVE_LENGTH)]

        expected_path = [((0, 0), (5, 5)), ((5, 5), (5, 9)), ((5, 9), (4, 9)), ((4, 9), (3, 8))]

        result_movements, result_path = self.path_converter.convert_path(self.path, self.robot)
        self.assertEqual(expected_path, result_path)
        self.assertEqual(' '.join(str(m) for m in expected_movements), ' '.join(str(m) for m in result_movements))
