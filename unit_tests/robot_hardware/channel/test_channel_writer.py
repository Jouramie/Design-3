from unittest import TestCase
from unittest.mock import Mock

from src.robot.hardware.channel import writer


class TestChannelWriter(TestCase):

    def setUp(self):
        self.message = '11111111'

    def test_when_write_then_calls_write_on_port(self):
        serial = Mock()
        serial.write = Mock()
        channel_writer = writer.ChannelWriter(serial)
        channel_writer.write(self.message)

        serial.write.assert_called_once_with(writer.wrapper(self.message))




