from unittest import TestCase

from src.d3_network.command import Command
from src.d3_network.encoder import DictionaryEncoder
from src.d3_network.network_exception import MessageNotReceivedYet


class TestDictionaryEncoder(TestCase):

    def test_when_encode_then_return_byte_string(self):
        message = {'command': Command.START}
        encoder = DictionaryEncoder()

        encoded_message = encoder.encode(message)

        self.assertEqual(encoded_message, b"0020{'command': 'start'}")

    def test_when_decode_then_return_dictionary(self):
        encoded_message = b"0022{'msg': 'hello world'}"
        encoder = DictionaryEncoder()

        message = encoder.decode(encoded_message)

        self.assertEqual(message, {'msg': 'hello world'})

    def test_given_incomplete_message_size_when_decode_then_throw_message_not_received_yet(self):
        encoded_message = b"002"
        encoder = DictionaryEncoder()

        self.assertRaises(MessageNotReceivedYet, encoder.decode, encoded_message)

    def test_given_incomplete_message_when_decode_then_throw_message_not_received_yet(self):
        encoded_message = b"0022{'msg': 'hell"
        encoder = DictionaryEncoder()

        self.assertRaises(MessageNotReceivedYet, encoder.decode, encoded_message)

    def test_given_message_in_two_part_when_decode_both_then_return_dictionary(self):
        first_encoded_message = b"0022{'msg': 'hell"
        second_encoded_message = b"o world'}"
        encoder = DictionaryEncoder()

        self.assertRaises(MessageNotReceivedYet, encoder.decode, first_encoded_message)
        message = encoder.decode(second_encoded_message)

        self.assertEqual(message, {'msg': 'hello world'})

    def test_given_two_messages_in_one_part_when_decode_two_times_then_return_both_dictionaries(self):
        encoded_messages = b"0022{'msg': 'hello world'}0020{'command': 'start'}"
        encoder = DictionaryEncoder()

        first_message = encoder.decode(encoded_messages)
        second_message = encoder.decode()

        self.assertEqual(first_message, {'msg': 'hello world'})
        self.assertEqual(second_message, {'command': 'start'})
