import ast

from .network_exception import MessageNotReceivedYet

MESSAGE_SIZE_BYTES = 4
MESSAGE_SIZE_FORMAT_TEMPLATE = '{length:0' + str(MESSAGE_SIZE_BYTES) + 'd}{msg}'


class Encoder(object):
    def encode(self, message) -> bytes:
        pass

    def decode(self, message: bytes = b""):
        pass


class DictionaryEncoder(Encoder):
    def __init__(self, encoding='ascii'):
        self.__encoding = encoding
        self.__buffer = b""

    def encode(self, message: dict) -> bytes:
        msg = str(message)
        string_message = MESSAGE_SIZE_FORMAT_TEMPLATE.format(length=len(msg), msg=msg)

        return string_message.encode(self.__encoding)

    def decode(self, message: bytes = b"") -> dict:
        self.__buffer += message

        if len(self.__buffer) <= MESSAGE_SIZE_BYTES:
            raise MessageNotReceivedYet()

        msg_len = int(self.__buffer.decode('ascii')[:4])

        if len(self.__buffer[MESSAGE_SIZE_BYTES:]) >= msg_len:
            msg = self.__buffer[MESSAGE_SIZE_BYTES:msg_len + MESSAGE_SIZE_BYTES]
            self.__buffer = self.__buffer[msg_len + MESSAGE_SIZE_BYTES:]
            return ast.literal_eval(msg.decode(self.__encoding))
        else:
            raise MessageNotReceivedYet()
