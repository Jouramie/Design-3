from unittest import TestCase

from src.robot.hardware.command.stm_command_builder import StmCommandBuilder
from src.robot.hardware.command.stm_command_definition.commands_to_stm import Target, Direction, Angle


class TestCommandBuilder(TestCase):

    def test_when_build_forward_then_correct_syntax(self):
        command = StmCommandBuilder()._move(Target.WHEELS_FORWARD, 5)
        self.assertEqual(b'\x3f\x00\x05', command)

    def test_when_build_left_then_correct_syntax(self):
        command = StmCommandBuilder()._move(Target.WHEELS_LEFT, 1111)
        self.assertEqual(b'\x31\x04\x57', command)

    def test_when_build_backward_then_correct_syntax(self):
        command = StmCommandBuilder()._move(Target.WHEELS_BACKWARD, 20)
        self.assertEqual(b'\x3b\x00\x14', command)

    def test_when_build_right_then_correct_syntax(self):
        command = StmCommandBuilder()._move(Target.WHEELS_RIGHT, 22222)
        self.assertEqual(b'\x32\x56\xce', command)

    def test_when_build_rotate_clockwise_then_correct_syntax(self):
        command = StmCommandBuilder().rotate_clockwise(Angle.NORTH)
        self.assertEqual(b'\x20\x00\x5a', command)

    def test_when_build_rotate_counter_clockwise_east_then_correct_syntax(self):
        command = StmCommandBuilder().rotate_counter_clockwise(Angle.EAST)
        self.assertEqual(b'\x21\x00\x00', command)

    def test_when_build_rotate_counter_clockwise_west_then_correct_syntax(self):
        command = StmCommandBuilder().rotate_counter_clockwise(Angle.WEST)
        self.assertEqual(b'\x21\x00\xb4', command)