from unittest import TestCase
from unittest.mock import Mock

from src.robot.hardware.channel import channel
from src.robot.hardware.channel.channel_listen_exception import ChannelException


class TestChannel(TestCase):

    def setUp(self):
        self.message = b'\x42\x30'
        self.expected_message = bytearray(b'\x42\x30\x8e')

    def test_when_listen_then_calls_readline(self):
        serial = Mock()
        serial.readline = Mock(return_value=self.message)
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
        channel_writer = channel.Channel(serial)
        channel_writer.write(self.message)

        serial.write.assert_called_once()

    def test_when_write_then_checksum_added(self):
        serial = Mock()
        serial.write = Mock()
        channel_writer = channel.Channel(serial)
        message = channel_writer.write(self.message)

        serial.write.assert_called_once_with(self.expected_message)
