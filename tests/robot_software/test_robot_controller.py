from unittest.mock import MagicMock
from unittest.mock import Mock

from src.robot_software import robot_controller


def test_when_start_controller_then_get_host_ip():
    network_scanner = MagicMock()
    ctrl = robot_controller.RobotController(network_scanner, MagicMock())

    ctrl.start()

    network_scanner.get_host_ip.assert_called_once()


def test_given_host_ip_when_start_controller_then_pair_with_host():
    host_ip = '10.42.0.78'
    network_scanner = Mock()
    network_scanner.attach_mock(Mock(return_value=host_ip), 'get_host_ip')
    network = MagicMock()
    ctrl = robot_controller.RobotController(network_scanner, network)

    ctrl.start()

    network.pair_with_host.assert_called_once_with(host_ip)
