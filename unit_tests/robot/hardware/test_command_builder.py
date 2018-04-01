from unittest import TestCase

from src.robot.hardware.command.command_builder import CommandBuilder
from src.robot.hardware.command.stm_command import CommandsToStm


class TestCommandBuilder(TestCase):

    def test_when_build_move_then_correct_syntax(self):
        command = CommandBuilder().move(CommandsToStm.WHEELS, 5, CommandsToStm.FORWARD)
        self.assertEqual(b'\x33\x05\xff', command)

    def test_when_build_another_move_then_correct_syntax(self):
        command = CommandBuilder().move(CommandsToStm.WHEELS, 20, CommandsToStm.LEFT)
        self.assertEqual(b'\x33\x14\x11', command)

    def test_when_build_rotate_then_correct_syntax(self):
        command = CommandBuilder().rotate(CommandsToStm.LEFT)
        self.assertEqual(b'\x20\x00\x11', command)


