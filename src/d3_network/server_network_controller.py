import socket
from src.d3_network.command import Command


class ServerNetworkController:

    def __init__(self, logger, port, encoder):
        self._logger = logger
        self._port = port
        self._encoder = encoder
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client = None

    def host_network(self):
        self._server.bind(('', self._port))

        while self._client is None:
            self._server.listen(5)
            self._client, address = self._server.accept()
            self._logger.info("{} connected".format(address))

            msg = {'msg': "ThAnKs YoU fOr CoNnEcTiNg !!!!1\n"}
            self._client.send(self._encoder.encode(msg))

    def send_start_command(self):
        msg = {'command': Command.START}
        self._client.send(self._encoder.encode(msg))

        self._logger.info("Start command sent!")

    def send_reset_command(self):
        msg = {'command': Command.RESET}
        self._client.send(self._encoder.encode(msg))

        self._logger.info("Start command sent!")
