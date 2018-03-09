from logging import Logger
from socket import socket

from .command import Command
from .encoder import Encoder


class NetworkController(object):
    def __init__(self, logger: Logger, port: int, encoder: Encoder):
        self._logger = logger
        self._port = port
        self._encoder = encoder
        self._socket: socket = None

    def _receive_data(self) -> dict:
        return self._encoder.decode(self._socket.recv(1024))

    def _send_command(self, command: Command, data: dict = None) -> None:
        if data is None:
            data = {}
        data['command'] = command
        self._socket.send(self._encoder.encode(data))
