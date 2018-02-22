from src.d3_network.encoder import DictionaryEncoder


def test_when_encode_then_return_byte_string():
    msg = {'msg': 'hello world'}
    encoder = DictionaryEncoder()

    byte = encoder.encode(msg)

    assert byte == b"{'msg': 'hello world'}"


def test_when_decode_then_return_dictionary():
    byte = b"{'msg': 'hello world'}"
    encoder = DictionaryEncoder()

    msg = encoder.decode(byte)

    assert msg == {'msg': 'hello world'}
