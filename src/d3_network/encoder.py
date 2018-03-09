import ast
from .network_exception import MessageNotReceivedYet


class Encoder(object):
    def encode(self, message) -> bytes:
        pass

    def decode(self, message: bytes):
        pass


class DictionaryEncoder(Encoder):
    def __init__(self, encoding='ascii'):
        self.__encoding = encoding
        self.__buffer = b""

    def encode(self, message: dict) -> bytes:
        string_message = str(message)

        return str(message).encode(self.__encoding)

    def decode(self, message: bytes) -> dict:
        self.__buffer += message

        if len(self.__buffer) <= 4:
            raise MessageNotReceivedYet()

        msg_len = int(self.__buffer.decode('ascii')[:4])

        if len(self.__buffer[4:]) == msg_len:
            return ast.literal_eval(self.__buffer[4:].decode(self.__encoding))
        else:
            raise MessageNotReceivedYet()
