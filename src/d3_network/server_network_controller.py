import socket
from logging import Logger

from src.d3_network.command import Command
from src.d3_network.encoder import Encoder


class ServerNetworkController:

    def __init__(self, logger: Logger, port: int, encoder: Encoder):
        self._logger = logger
        self._port = port
        self._encoder = encoder
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client = None

    def host_network(self) -> None:
        self._server.bind(('', self._port))

        while self._client is None:
            self._server.listen(5)
            self._client, address = self._server.accept()
            self._logger.info("{} connected".format(address))

            msg = {'msg': "ThAnKs YoU fOr CoNnEcTiNg !!!!1\n"}
            self._client.send(self._encoder.encode(msg))

    def send_start_command(self) -> None:
        msg = {'command': Command.START}
        self._client.send(self._encoder.encode(msg))

        self._logger.info("Start command sent!")

    def send_reset_command(self) -> None:
        msg = {'command': Command.RESET}
        self._client.send(self._encoder.encode(msg))

        self._logger.info("Start command sent!")
