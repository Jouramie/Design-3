from unittest import TestCase

from src.d3_network.command import Command
from src.robot.hardware.command.stm_command_definition import commands_to_stm
from src.robot.hardware.command.stm_command_factory import StmCommand


class TestStmCommandFactory(TestCase):

    def test_when_build_forward_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.MOVE_FORWARD, 'amplitude': 5.0})
        self.assertEqual(b'\x3f\x00\x32', command)

    def test_when_build_left_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.MOVE_LEFT, 'amplitude': 111.0})
        self.assertEqual(b'\x31\x04\x56', command)

    def test_when_build_backward_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.MOVE_BACKWARD, 'amplitude': 20.0})
        self.assertEqual(b'\x3b\x00\xc8', command)

    def test_when_build_right_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.MOVE_RIGHT, 'amplitude': 222.0})
        self.assertEqual(b'\x32\x08\xac', command)

    def test_when_build_rotate_clockwise_north_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.MOVE_ROTATE, 'amplitude': -90.0})
        self.assertEqual(b'\x20\x00\x5a', command)

    def test_when_build_rotate_clockwise_east_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.MOVE_ROTATE, 'amplitude': 0.0})
        self.assertEqual(b'\x21\x00\x00', command)

    def test_when_build_rotate_counter_clockwise_west_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.MOVE_ROTATE, 'amplitude': -180.0})
        self.assertEqual(b'\x20\x00\xb4', command)

    def test_when_build_rotate_counter_clockwise_sw_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.MOVE_ROTATE, 'amplitude': 45.0})
        self.assertEqual(b'\x21\x00\x2d', command)

    def test_when_build_rotate_clockwise_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.MOVE_ROTATE, 'amplitude': 90.0})
        self.assertEqual(b'\x21\x00\x5a', command)

    def test_when_build_rotate_counter_clockwise_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.MOVE_ROTATE, 'amplitude': -90.0})
        self.assertEqual(b'\x20\x00\x5a', command)

    def test_when_build_ir_signal_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.INFRARED_SIGNAL})
        self.assertEqual(commands_to_stm.Command.IR_SIGNAL.value, command)

    def test_when_build_grab_cube_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.GRAB})
        self.assertEqual(commands_to_stm.Command.GRAB_CUBE.value, command)

    def test_when_build_can_grab_cube_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.CAN_I_GRAB})
        self.assertEqual(commands_to_stm.Command.CAN_GRAB_CUBE.value, command)

    def test_when_build_drop_cube_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.DROP})
        self.assertEqual(commands_to_stm.Command.DROP_CUBE.value, command)

    def test_when_build_light_led_then_correct_syntax(self):
        command = StmCommand.factory({'command': Command.END_SIGNAL})
        self.assertEqual(commands_to_stm.Command.LIGHT_IT_UP.value, command)


