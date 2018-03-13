import os
import pty
from unittest import TestCase
from unittest.mock import Mock

from serial import Serial

from src.robot_hardware.channel import writer


class TestChannelWriter(TestCase):

    def setUp(self):
        self.message = '11111111'
        self.master, self.port = create_virtual_serial_device()

    def test_when_write_then_calls_write_on_port(self):
        serial = Mock()
        serial.write = Mock()
        channel_writer = writer.ChannelWriter(serial)
        channel_writer.write(self.message)

        serial.write.assert_called_once_with(writer.wrapper(self.message))

    def test_when_write_then_message_written(self):
        serial = Serial(self.port)
        channel_writer = writer.ChannelWriter(serial)
        channel_writer.write(self.message)
        msg = os.read(self.master, 16)

        self.assertEqual(writer.wrapper(self.message), msg)

def create_virtual_serial_device():
    master, slave = pty.openpty()
    port = os.ttyname(slave)
    return master, port



