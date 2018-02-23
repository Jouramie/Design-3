from src.d3_network.encoder import DictionaryEncoder
from src.d3_network.command import Command


def test_when_encode_then_return_byte_string():
    msg = {'command': Command.START}
    encoder = DictionaryEncoder()

    byte = encoder.encode(msg)

    assert byte == b"{'command': 'start'}"


def test_when_decode_then_return_dictionary():
    byte = b"{'msg': 'hello world'}"
    encoder = DictionaryEncoder()

    msg = encoder.decode(byte)

    assert msg == {'msg': 'hello world'}
