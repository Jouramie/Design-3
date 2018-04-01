from unittest import TestCase

from src.robot.hardware.command.stm_command_builder import StmCommandBuilder
from src.robot.hardware.command.stm_command_definition.commands_to_stm import Target, Direction


class TestCommandBuilder(TestCase):

    def test_when_build_move_then_correct_syntax(self):
        command = StmCommandBuilder()._move(Target.WHEELS, 5, Direction.FORWARD)
        self.assertEqual(b'\x33\x05\xff', command)

    def test_when_build_another_move_then_correct_syntax(self):
        command = StmCommandBuilder()._move(Target.WHEELS, 20, Direction.LEFT)
        self.assertEqual(b'\x33\x14\x11', command)

    def test_when_build_rotate_then_correct_syntax(self):
        command = StmCommandBuilder().rotate(Direction.LEFT)
        self.assertEqual(b'\x20\x00\x11', command)
