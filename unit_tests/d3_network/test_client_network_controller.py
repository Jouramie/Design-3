
from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from src.d3_network import client_network_controller as client_network_ctl
from src.d3_network.command import Command
from src.d3_network.network_exception import MessageNotReceivedYet


class TestClientNetworkController(TestCase):

    @patch('src.d3_network.client_network_controller.socket')
    def test_when_pair_with_host_then_connect(self, socket):
        port = 1234
        host_ip = '255.255.255.255'
        client = MagicMock()
        socket.return_value = client
        encoder = MagicMock()
        encoder.attach_mock(Mock(return_value={'command': Command.HELLO}), 'decode')
        network_controller = client_network_ctl.ClientNetworkController(MagicMock(), port, encoder)

        network_controller.pair_with_host(host_ip)

        client.connect.assert_called_once_with((host_ip, port))

    @patch('src.d3_network.client_network_controller.socket')
    def test_given_paired_network_controller_when_wait_start_command_then_receive_communication(self, socket):
        client = MagicMock()
        socket.return_value = client
        encoder = MagicMock()
        encoder.attach_mock(Mock(return_value={'command': Command.START}), 'decode')
        network_controller = client_network_ctl.ClientNetworkController(MagicMock(), MagicMock(), encoder)

        network_controller.wait_start_command()

        client.recv.assert_called_once()

    @patch('src.d3_network.client_network_controller.socket')
    def test_given_paired_network_controller_when_wait_start_command_then_decode_received_communication(self, socket):
        encoder = MagicMock()
        encoder.attach_mock(Mock(return_value={'command': Command.START}), 'decode')
        received_bytes = b"{'msg': 'hello'}"
        client = MagicMock()
        client.attach_mock(Mock(return_value=received_bytes), 'recv')
        socket.return_value = client
        network_controller = client_network_ctl.ClientNetworkController(MagicMock(), MagicMock(), encoder)

        network_controller.wait_start_command()

        encoder.decode.assert_called_once_with(received_bytes)

    @patch('src.d3_network.client_network_controller.socket')
    def test_given_paired_network_controller_when_wait_start_command_timeout_then_retry_receive(self, socket):
        encoder = MagicMock()
        encoder.attach_mock(Mock(return_value={'command': Command.START}), 'decode')
        client = MagicMock()
        client.attach_mock(Mock(side_effect=[MessageNotReceivedYet, None]), 'recv')
        socket.return_value = client
        network_controller = client_network_ctl.ClientNetworkController(MagicMock(), MagicMock(), encoder)

        network_controller.wait_start_command()

        self.assertEqual(2, client.recv.call_count)
