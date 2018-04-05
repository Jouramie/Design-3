from unittest import TestCase

from src.robot.hardware.command.stm_command_builder import StmCommandBuilder
from src.robot.hardware.command.stm_command_definition.commands_to_stm import Target


class TestCommandBuilder(TestCase):

    def test_when_build_forward_then_correct_syntax(self):
        command = StmCommandBuilder().forward(5)
        self.assertEqual(b'\x3f\x00\x32', command)

    def test_when_build_left_then_correct_syntax(self):
        command = StmCommandBuilder().left(111)
        self.assertEqual(b'\x31\x04\x56', command)

    def test_when_build_backward_then_correct_syntax(self):
        command = StmCommandBuilder()._move(Target.WHEELS_BACKWARD, 20)
        self.assertEqual(b'\x3b\x00\x14', command)

    def test_when_build_right_then_correct_syntax(self):
        command = StmCommandBuilder().right(222)
        self.assertEqual(b'\x32\x08\xac', command)

    def test_when_build_rotate_clockwise_north_then_correct_syntax(self):
        command = StmCommandBuilder().rotate(-90)
        self.assertEqual(b'\x20\x00\x5a', command)

    def test_when_build_rotate_clockwise_east_then_correct_syntax(self):
        command = StmCommandBuilder().rotate(0)
        self.assertEqual(b'\x21\x00\x00', command)

    def test_when_build_rotate_counter_clockwise_west_then_correct_syntax(self):
        command = StmCommandBuilder().rotate(-180)
        self.assertEqual(b'\x20\x00\xb4', command)

    def test_when_build_rotate_counter_clockwise_sw_then_correct_syntax(self):
        command = StmCommandBuilder().rotate(45)
        self.assertEqual(b'\x21\x00\x2d', command)

    def test_when_build_rotate_clockwise_then_correct_syntax(self):
        command = StmCommandBuilder().rotate(90)
        self.assertEqual(b'\x21\x00\x5a', command)

    def test_when_build_rotate_counter_clockwise_then_correct_syntax(self):
        command = StmCommandBuilder().rotate(-90)
        self.assertEqual(b'\x20\x00\x5a', command)