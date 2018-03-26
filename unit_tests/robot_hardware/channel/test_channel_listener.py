from unittest import TestCase
from unittest.mock import Mock

from src.robot.hardware.channel import channel
from src.robot.hardware.channel.channel_listen_exception import ChannelException


class TestChannelListener(TestCase):

    def setUp(self):
        self.message = '11111111'

    def test_when_listen_then_calls_readline(self):
        serial = Mock()
        serial.readline = Mock(return_value=self.message.encode())
        channel_listener = channel.Channel(serial)
        channel_listener.listen()

        serial.readline.assert_called_once()

    def test_when_closed_listen_raises_exception(self):
        serial = Mock()
        serial.isOpen = Mock(return_value=False)
        channel_listener = channel.Channel(serial)
        channel_listener.listen()

        self.assertRaises(ChannelException)

    def test_when_write_then_calls_write_on_port(self):
        serial = Mock()
        serial.write = Mock()
        channel_writer = channel.ChannelWriter(serial)
        channel_writer.write(self.message)

        serial.write.assert_called_once_with(self.message)

