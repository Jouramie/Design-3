from unittest import TestCase
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

from src.d3_network import server_network_controller as server_network_ctl
from src.domain.path_calculator.action import Start


class TestSocketServerNetworkController(TestCase):

    @patch('src.d3_network.server_network_controller.socket')
    def test_given_connected_client_when_send_start_command_then_send_encoded_message(self, socket):
        client = MagicMock()
        encoder = MagicMock()
        encoded_msg = b"0017{'msg': 'qwerty'}"
        encoder.attach_mock(Mock(return_value=encoded_msg), 'encode')
        serv_network_ctl = server_network_ctl.SocketServerNetworkController(MagicMock(), MagicMock(), encoder)
        serv_network_ctl._socket = client

        serv_network_ctl.send_action(Start())

        client.send.assert_called_once_with(encoded_msg)
