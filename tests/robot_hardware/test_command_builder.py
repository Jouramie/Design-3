from unittest import TestCase

from src.robot_hardware.command import Command
from src.robot_hardware.command_builder import CommandBuilder


class TestCommandBuilder(TestCase):

    def setUp(self):
        self.vx = 5
        self.vy = 5

    def test_when_build_move_then_correct_syntax(self):
        command = CommandBuilder().move(self.vx, self.vy, Command.forward, Command.right)
        self.assertEqual('M55FR', command)

    def test_when_build_forward_then_correct_syntax(self):
        command = CommandBuilder().forward(self.vx, self.vy, Command.right)
        self.assertEqual('M55FR', command)

    def test_when_build_backward_then_correct_syntax(self):
        command = CommandBuilder().backward(self.vx, self.vy, Command.right)
        self.assertEqual('M55BR', command)
