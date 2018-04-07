from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.d3_network.command import Command
from src.robot import robot_controller
from src.robot.hardware.command.stm_command_builder import StmCommand
from src.robot.hardware.command.stm_command_definition import commands_from_stm


class TestRobotController(TestCase):
    def test_when_start_controller_then_get_host_ip(self):
        network_scanner = MagicMock()
        ctrl = robot_controller.RobotController(MagicMock(), network_scanner, MagicMock(), MagicMock())

        ctrl._start()

        network_scanner.get_host_ip.assert_called_once()

    def test_given_host_ip_when_start_controller_then_pair_with_host(self):
        host_ip = '10.42.0.78'
        network_scanner = Mock()
        network_scanner.attach_mock(Mock(return_value=host_ip), 'get_host_ip')
        network_ctrl = MagicMock()
        network_ctrl.attach_mock(Mock(return_value=dict({'command': 'end-signal'})), 'wait_message')
        ctrl = robot_controller.RobotController(MagicMock(), network_scanner, network_ctrl, MagicMock())

        ctrl._start()

        network_ctrl.pair_with_host.assert_called_once_with(host_ip)

    def test_when_start_controller_then_wait_start_command(self):
        network_ctrl = MagicMock()
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())

        ctrl._start()

        network_ctrl.wait_start_command.assert_called_once()

    def test_when_receive_message_from_stm_then_append_it_to_queue(self):
        channel = MagicMock()
        channel.attach_mock(Mock(return_value=commands_from_stm.Feedback(
            commands_from_stm.Message.TASK_RECEIVED_ACK.value)), 'receive_message')
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())

        ctrl.receive_stm_command()

        self.assertEqual(1, ctrl._stm_responses_queue.qsize())

    def test_when_send_movement_command_then_send_via_channel(self):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.receive_message = Mock(return_value=commands_from_stm.Message.SUCCESSFULL_TASK.value)
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.send_command_to_stm(StmCommand.factory({'command': Command.MOVE_BACKWARD, 'amplitude': 200}))

        channel.send_command.assert_called_once_with(bytearray(b'\x3b\x07\xd0'))

    def test_when_add_movement_to_queue_then_movement_added(self):
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}

        ctrl.add_stm_command_to_queue(command)

        self.assertEqual(StmCommand.factory(command), ctrl._stm_commands_todo.pop())
