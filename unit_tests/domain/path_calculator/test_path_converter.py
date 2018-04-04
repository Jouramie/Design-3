from unittest import TestCase
from unittest.mock import MagicMock

from src.domain.path_calculator.direction import Direction
from src.domain.path_calculator.direction import FORTY_FIVE_DEGREES_MOVE_LENGTH
from src.domain.path_calculator.direction import NINETY_DEGREES_MOVE_LENGTH
from src.domain.path_calculator.path_converter import PathConverter


class TestPathConverter(TestCase):
    def setUp(self):
        self.path_converter = PathConverter(MagicMock())
        self.path = []
        self.path.append((0, 0))

    def test_when_convert_north_direction_then_command_length_is_one(self):
        self.path.append(Direction.NORTH.value)

        expected = [(NINETY_DEGREES_MOVE_LENGTH, 'NORTH')], [((0, 0), (0, -1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_south_direction_then_command_length_is_one(self):
        self.path.append(Direction.SOUTH.value)

        expected = [(NINETY_DEGREES_MOVE_LENGTH, 'SOUTH')], [((0, 0), (0, 1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_east_direction_then_command_length_is_one(self):
        self.path.append(Direction.EAST.value)

        expected = [(NINETY_DEGREES_MOVE_LENGTH, 'EAST')], [((0, 0), (-1, 0))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_west_direction_then_command_length_is_one(self):
        self.path.append(Direction.WEST.value)

        expected = [(NINETY_DEGREES_MOVE_LENGTH, 'WEST')], [((0, 0), (1, 0))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_north_east_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.NORTH_EAST.value)

        expected = [(FORTY_FIVE_DEGREES_MOVE_LENGTH, 'NORTH_EAST')], [((0, 0), (-1, -1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_south_east_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.SOUTH_EAST.value)

        expected = [(FORTY_FIVE_DEGREES_MOVE_LENGTH, 'SOUTH_EAST')], [((0, 0), (-1, 1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_north_west_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.NORTH_WEST.value)

        expected = [(FORTY_FIVE_DEGREES_MOVE_LENGTH, 'NORTH_WEST')], [((0, 0), (1, -1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_south_west_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.SOUTH_WEST.value)

        expected = [(FORTY_FIVE_DEGREES_MOVE_LENGTH, 'SOUTH_WEST')], [((0, 0), (1, 1))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_example_path_then_received_corresponding_commands(self):
        self.path = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (4, 9), (3, 8)]
        expected = [(16, 'SOUTH_WEST'), (40, 'SOUTH'), (10, 'EAST'), (4, 'NORTH_EAST')], \
                   [((1, 1), (5, 5)), ((5, 5), (5, 9)), ((5, 9), (4, 9)), ((4, 9), (3, 8))]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))
