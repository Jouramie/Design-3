from unittest import TestCase

from src.d3_network.encoder import DictionaryEncoder
from src.d3_network.command import Command


class TestDictionaryEncoder(TestCase):

    def test_when_encode_then_return_byte_string(self):
        msg = {'command': Command.START}
        encoder = DictionaryEncoder()

        byte = encoder.encode(msg)

        self.assertEqual(byte, b"{'command': 'start'}")

    def test_when_decode_then_return_dictionary(self):
        byte = b"{'msg': 'hello world'}"
        encoder = DictionaryEncoder()

        msg = encoder.decode(byte)

        self.assertEqual(msg, {'msg': 'hello world'})
