from unittest import TestCase

from src.robot.hardware.command.command_from_stm import CommandFromStm
from src.robot.hardware.command.not_a_country_command_exception import NotACountryCommandException
from src.robot.hardware.message_corrupted_exception import MessageCorruptedException


class TestCommandConverter(TestCase):

    def setUp(self):
        self.country_code_message = b'\xb0\x04\x4c'
        self.other_country_code_message = b'\xb0\x75\xdb'
        self.wrong_country_code_message = b'\xb1\x04\x4b'

    def test_given_infra_red_signal_then_extract_country_code(self):
        command = CommandFromStm(self.country_code_message)
        self.assertEqual(command.get_country_code(), self.country_code_message[1])

    def test_given_another_infra_red_signal_then_extract_country_code(self):
        command = CommandFromStm(self.other_country_code_message)
        self.assertEqual(command.get_country_code(), self.other_country_code_message[1])

    # def test_given_wrong_infra_red_signal_command_then_raises_exception_on_validation(self):
    #     self.assertRaises(MessageCorruptedException, CommandFromStm(self.wrong_country_code_message)._validate)

    def test_given_wrong_infra_red_signal_command_then_raises_exception_when_getting_country_id(self):
        self.assertRaises(NotACountryCommandException, CommandFromStm(self.wrong_country_code_message).get_country_code)
