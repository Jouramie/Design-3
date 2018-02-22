import socket
from src.d3_network.command import Command


class ClientNetworkController:

    def __init__(self, logger, port, encoder):
        self._logger = logger
        self._port = port
        self._encoder = encoder
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def pair_with_host(self, host_ip):
        self._client.connect((host_ip, self._port))
        msg = self._client.recv(1024)

        self._logger.info(self._encoder.decode(msg))

    def wait_start_command(self, callback):
        msg = self._encoder.decode(self._client.recv(1024))
        self._logger.info(msg)

        if msg['command'] == Command.START:
            callback()
