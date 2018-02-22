from unittest.mock import MagicMock
from unittest.mock import Mock

from src.robot_software import robot_controller


def test_when_start_controller_then_get_host_ip():
    network_scanner = MagicMock()
    ctrl = robot_controller.RobotController(MagicMock(), network_scanner, MagicMock())

    ctrl.start()

    network_scanner.get_host_ip.assert_called_once()


def test_given_host_ip_when_start_controller_then_pair_with_host():
    host_ip = '10.42.0.78'
    network_scanner = Mock()
    network_scanner.attach_mock(Mock(return_value=host_ip), 'get_host_ip')
    network_ctrl = MagicMock()
    ctrl = robot_controller.RobotController(MagicMock(), network_scanner, network_ctrl)

    ctrl.start()

    network_ctrl.pair_with_host.assert_called_once_with(host_ip)


def test_when_start_controller_then_wait_start_signal():
    network_ctrl = MagicMock()
    ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl)

    ctrl.start()

    network_ctrl.wait_start_command.assert_called_once_with(ctrl.on_receive_start_command)

