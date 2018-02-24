import ast


class Encoder:
    def encode(self, message) -> bytes:
        pass

    def decode(self, message: bytes):
        pass


class DictionaryEncoder(Encoder):
    def __init__(self, encoding='ascii'):
        self.encoding = encoding

    def encode(self, message: dict) -> bytes:
        return str(message).encode(self.encoding)

    def decode(self, message: bytes) -> dict:
        return ast.literal_eval(message.decode(self.encoding))
