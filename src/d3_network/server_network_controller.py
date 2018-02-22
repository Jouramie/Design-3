import socket
from src.d3_network.command import Command


class NetworkController:

    def __init__(self, logger, port, encoding='ascii'):
        self._logger = logger
        self._port = port
        self._encoding = encoding
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def host_network(self):
        self._server.bind(('', self._port))

        client = False
        while not client:
            self._server.listen(5)
            client, address = self._server.accept()
            self._logger.info("{} connected".format(address))

            msg = "ThAnKs YoU fOr CoNnEcTiNg !!!!1\n"
            client.send(msg.encode(self._encoding))

    def send_start_command(self):
        msg = {'command': Command.START}
        self._server.send(self._encode(msg))

    def _encode(self, msg):
        return str(msg).encode(self._encoding)

    def _decode(self, msg):
        return msg.decode(self._encoding)

