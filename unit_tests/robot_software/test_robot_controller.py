from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from src.robot import robot_controller
from src.robot.hardware.command.stm_command import CommandsToStm


class TestRobotController(TestCase):

    @patch('src.robot.robot_controller.time')
    def test_when_start_controller_then_get_host_ip(self, time):
        network_scanner = MagicMock()
        ctrl = robot_controller.RobotController(MagicMock(), network_scanner, MagicMock(), MagicMock())

        ctrl.start()

        network_scanner.get_host_ip.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_given_host_ip_when_start_controller_then_pair_with_host(self, time):
        host_ip = '10.42.0.78'
        network_scanner = Mock()
        network_scanner.attach_mock(Mock(return_value=host_ip), 'get_host_ip')
        network_ctrl = MagicMock()
        ctrl = robot_controller.RobotController(MagicMock(), network_scanner, network_ctrl, MagicMock())

        ctrl.start()

        network_ctrl.pair_with_host.assert_called_once_with(host_ip)

    @patch('src.robot.robot_controller.time')
    def test_when_start_controller_then_wait_start_command(self, time):
        network_ctrl = MagicMock()
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())

        ctrl.start()

        network_ctrl.wait_start_command.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_when_receive_country_code_then_return_country_code(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.receive_message = Mock(return_value=43)
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.receive_country_code()

        channel.receive_message.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_when_send_grab_cube_then_send_via_channel(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.send_command= Mock()
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.send_grab_cube()

        channel.send_command.assert_called_once_with(CommandsToStm.GRAB_CUBE.value)

    @patch('src.robot.robot_controller.time')
    def test_when_send_drop_cube_then_send_via_channel(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.send_command= Mock()
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.send_drop_cube()

        channel.send_command.assert_called_once_with(CommandsToStm.DROP_CUBE.value)

    @patch('src.robot.robot_controller.time')
    def test_when_ask_if_can_grab_cube_then_send_via_channel(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.send_command= Mock()
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.ask_if_can_grab_cube()

        channel.send_command.assert_called_once_with(CommandsToStm.CAN_GRAB_CUBE.value)
