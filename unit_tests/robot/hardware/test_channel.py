from unittest import TestCase
from unittest.mock import Mock

from src.robot.hardware.channel import Channel
from src.robot.hardware.channel_exception import ChannelException
from src.robot.hardware.command.stm_command_definition import commands_from_stm


class TestChannel(TestCase):

    def setUp(self):
        self.serial = Mock()
        self.message = b'\x42\x30\x00'
        self.expected_sent_message = bytearray(b'\x42\x30\x00\x8e')
        self.other_message = b'\x41\x30\x00'
        self.other_expected_message = bytearray(b'\x41\x30\x00\x8f')
        self.send_again_with_checksum = bytearray(b'\x46\x41\x12\x67')
        self.send_drop_cube = bytearray(b'\xdc\x12\x23')
        self.drop_cube_checksum = 0xef

    def test_when_receive_message_then_calls_read(self):
        self.serial.read = Mock(return_value=commands_from_stm.Message.SUCCESSFULL_TASK.value)
        channel = Channel(self.serial)

        channel.receive_message()

        self.serial.read.assert_called_with(commands_from_stm.Message.BYTES_TO_READ.value)

    def test_when_receive_open_close_message_then_return_hey_type(self):
        self.serial.read = Mock(return_value=commands_from_stm.Message.OPEN_CLOSE_MSG.value)
        channel = Channel(self.serial)

        self.assertEqual(commands_from_stm.Feedback.HEY, channel.receive_message().type)

    def test_when_receive_nothing_message_then_return_hey_type(self):
        self.serial.read = Mock(return_value=commands_from_stm.Message.NOTHING.value)
        channel = Channel(self.serial)

        msg = channel.receive_message()

        self.assertEqual(commands_from_stm.Feedback.HEY, msg.type)

    def test_when_receive_country_code_then_return_country_type(self):
        self.serial.read = Mock(return_value=bytearray(b'\xb0\x12\x00\x3e'))
        channel = Channel(self.serial)

        msg = channel.receive_message()

        self.assertEqual(commands_from_stm.Feedback.COUNTRY, msg.type)

    def test_when_receive_country_code_then_return_country_code(self):
        self.serial.read = Mock(return_value=bytearray(b'\xb0\x12\x00\x3e'))
        channel = Channel(self.serial)

        msg = channel.receive_message()

        self.assertEqual(0x12, msg.country)


    def test_when_closed_listen_raises_exception(self):
        self.serial.isOpen = Mock(return_value=False)
        self.serial.read = Mock(return_value=bytearray(b'\xb0\x12\x00\x3e'))
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

        self.serial.write.assert_called_once_with(self.expected_sent_message)

    def test_given_another_message_when_write_then_correct_checksum_added(self):
        self.serial.write = Mock()
        channel = Channel(self.serial)

        channel.send_command(self.other_message)

        self.serial.write.assert_called_once_with(self.other_expected_message)

    def test_when_calculate_checksum_right_checksum_returned(self):
        self.serial.write = Mock()
        channel = Channel(self.serial)

        self.assertEqual(self.drop_cube_checksum, channel.calculate_checksum(self.send_drop_cube))
