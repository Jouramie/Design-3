from unittest import TestCase
from unittest.mock import Mock

from src.robot.hardware.channel import Channel
from src.robot.hardware.channel_exception import ChannelException


class TestChannel(TestCase):

    def setUp(self):
        self.serial = Mock()
        self.message = b'\x42\x30\x00'
        self.expected_message = bytearray(b'\x42\x30\x00\x8e')
        self.other_message = b'\x41\x30\x00'
        self.other_expected_message = bytearray(b'\x41\x30\x00\x8f')
        self.send_again_with_checksum = bytearray(b'\x46\x41\x12\x67')
        self.send_drop_cube = bytearray(b'\xdc\x12\x23')
        self.drop_cube_checksum = 0xef

    def test_when_listen_then_calls_readline(self):
        self.serial.read = Mock(return_value=self.message)
        channel = Channel(self.serial)

        channel.receive_message()

        self.serial.read.assert_called_with(4)

    def test_when_closed_listen_raises_exception(self):
        self.serial.isOpen = Mock(return_value=False)
        channel = Channel(self.serial)

        channel.receive_message()

        self.assertRaises(ChannelException)

    def test_when_write_then_calls_write_on_port(self):
        self.serial.write = Mock()
        channel = Channel(self.serial)

        channel.send_command(self.message)

        self.serial.write.assert_called_once()

    def test_given_a_message_when_write_then_checksum_added(self):
        self.serial.write = Mock()
        channel = Channel(self.serial)

        channel.send_command(self.message)

        self.serial.write.assert_called_once_with(self.expected_message)

    def test_given_another_message_when_write_then_correct_checksum_added(self):
        self.serial.write = Mock()
        channel = Channel(self.serial)

        channel.send_command(self.other_message)

        self.serial.write.assert_called_once_with(self.other_expected_message)


    def test_when_ask_again_then_calls_write_on_port_with_corresponding_mesage(self):
        self.serial.write = Mock()
        channel = Channel(self.serial)

        channel.ask_repeat()

        self.serial.write.assert_called_once_with(self.send_again_with_checksum)

    def test_when_calculate_checksum_right_checksum_returned(self):
        self.serial.write = Mock()
        channel = Channel(self.serial)

        self.assertEqual(self.drop_cube_checksum, channel.calculate_checksum(self.send_drop_cube))
