from unittest import TestCase
from unittest.mock import Mock

from src.robot_software.channel import listener
from src.robot_software.channel.channel_listener_exception import ChannelListenerException


class TestChannelListener(TestCase):
    def setUp(self):
        self.message = '11111111'

    def test_when_listen_then_calls_readline(self):
        serial = Mock()
        serial.readline = Mock(return_value=self.message.encode())
        channel_listener = listener.ChannelListener(serial)
        channel_listener.listen()

        serial.readline.assert_called_once()

    def test_when_closed_listen_raises_exception(self):
        serial = Mock()
        serial.isOpen = Mock(return_value=False)
        channel_listener = listener.ChannelListener(serial)
        channel_listener.listen()

        self.assertRaises(ChannelListenerException)
