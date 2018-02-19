from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import call

from src.robot_software import robot_controller


def test_when_start_controller_then_get_host_ip():
    network_scanner = MagicMock()
    network = MagicMock()
    ctrl = robot_controller.RobotController(network_scanner, network)

    ctrl.start()

    assert network_scanner.method_calls == [call.get_host_ip()]


def test_given_host_ip_when_start_controller_then_pair_with_host():
    host_ip = '10.42.0.78'
    network_scanner = Mock()
    get_host_ip = Mock()
    get_host_ip.return_value = host_ip
    network_scanner.attach_mock(get_host_ip, 'get_host_ip')

    network = MagicMock()
    ctrl = robot_controller.RobotController(network_scanner, network)

    ctrl.start()

    assert network.method_calls == [call.pair_with_host(host_ip)]
