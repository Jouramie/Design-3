from logging import Logger
import socket
from typing import Callable

from .command import Command
from .encoder import Encoder


class ClientNetworkController(object):

    def __init__(self, logger: Logger, port: int, encoder: Encoder):
        self._logger = logger
        self._port = port
        self._encoder = encoder
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def pair_with_host(self, host_ip: str) -> None:
        self._client.connect((host_ip, self._port))
        msg = self._client.recv(1024)

        self._logger.info(self._encoder.decode(msg))

    def wait_start_command(self, callback: Callable[[], None]) -> None:
        msg = self._encoder.decode(self._client.recv(1024))
        self._logger.info(msg)

        if msg['command'] == Command.START:
            callback()
