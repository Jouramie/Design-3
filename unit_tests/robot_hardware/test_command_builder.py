from unittest import TestCase

from src.robot.hardware.command import CommandsToStm
from src.robot.hardware.command_builder import CommandBuilder


class TestCommandBuilder(TestCase):

    def setUp(self):
        self.vx = 5
        self.vy = 5

    def test_when_build_move_then_correct_syntax(self):
        command = CommandBuilder().move(self.vx, self.vy, CommandsToStm.FORWARD, CommandsToStm.RIGHT)
        self.assertEqual('M55FR', command)

    def test_when_build_forward_then_correct_syntax(self):
        command = CommandBuilder().forward(self.vx, self.vy, CommandsToStm.RIGHT)
        self.assertEqual('M55FR', command)

    def test_when_build_backward_then_correct_syntax(self):
        command = CommandBuilder().backward(self.vx, self.vy, CommandsToStm.RIGHT)
        self.assertEqual('M55BR', command)
