from unittest import TestCase
from src.domain.path_calculator.direction import Direction
from src.domain.path_calculator.path_converter import PathConverter

NINETY_DEGREES_MOVE_LENGTH = 1
FORTY_FIVE_DEGREES_MOVE_LENGTH = 1.4142


class TestPathConverter(TestCase):
    def setUp(self):
        self.path_converter = PathConverter()
        self.path = []
        self.path.append((0, 0))

    def test_when_convert_north_direction_then_command_length_is_one(self):
        self.path.append(Direction.NORTH.value)

        expected = [(NINETY_DEGREES_MOVE_LENGTH, 'NORTH')]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_south_direction_then_command_length_is_one(self):
        self.path.append(Direction.SOUTH.value)

        expected = [(NINETY_DEGREES_MOVE_LENGTH, 'SOUTH')]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_east_direction_then_command_length_is_one(self):
        self.path.append(Direction.EAST.value)

        expected = [(NINETY_DEGREES_MOVE_LENGTH, 'EAST')]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_west_direction_then_command_length_is_one(self):
        self.path.append(Direction.WEST.value)

        expected = [(NINETY_DEGREES_MOVE_LENGTH, 'WEST')]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_north_east_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.NORTH_EAST.value)

        expected = [(FORTY_FIVE_DEGREES_MOVE_LENGTH, 'NORTH_EAST')]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_south_east_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.SOUTH_EAST.value)

        expected = [(FORTY_FIVE_DEGREES_MOVE_LENGTH, 'SOUTH_EAST')]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_north_west_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.NORTH_WEST.value)

        expected = [(FORTY_FIVE_DEGREES_MOVE_LENGTH, 'NORTH_WEST')]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_south_west_direction_then_command_length_is_radical_two(self):
        self.path.append(Direction.SOUTH_WEST.value)

        expected = [(FORTY_FIVE_DEGREES_MOVE_LENGTH, 'SOUTH_WEST')]

        self.assertEqual(expected, self.path_converter.convert_path(self.path))

    def test_when_convert_example_path_then_received_corresponding_commands(self):
        self.path = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (4, 9), (3, 8)]
        expected = '[(5.6568, \'SOUTH_WEST\'), (4, \'SOUTH\'), (1, \'EAST\'), (1.4142, \'NORTH_EAST\')]'

        self.assertEqual(expected, self.path_converter.convert_path(self.path).__str__())
