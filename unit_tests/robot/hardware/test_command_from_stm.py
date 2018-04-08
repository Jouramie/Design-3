from unittest import TestCase

from src.robot.hardware.command.command_from_stm import CommandFromStm
from src.robot.hardware.command.stm_command_definition import commands_from_stm


class TestCommandFromStm(TestCase):

    def test_when_create_command_then_created(self):
        command = CommandFromStm(b'\xfc\x12\x34\xbe')

        self.assertEqual(command.command, bytearray(b'\xfc\x12\x34\xbe'))

    def test_when_create_command_then_target_tracked(self):
        command = CommandFromStm(commands_from_stm.Message.SUCCESSFULL_TASK.value)

        self.assertEqual(command.target, commands_from_stm.Target.TASK_SUCCESS.value)

    def test_when_create_command_validate(self):
        command = CommandFromStm(commands_from_stm.Message.SUCCESSFULL_TASK.value)

        self.assertEqual(True, command._validate())

