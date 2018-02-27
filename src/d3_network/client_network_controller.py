from logging import Logger
import socket
from .command import Command
from .encoder import Encoder
from .network_exception import NetworkException
from .network_controller import NetworkController


class ClientNetworkController(NetworkController):

    def __init__(self, logger: Logger, port: int, encoder: Encoder):
        super().__init__(logger, port, encoder)
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(5)

    def pair_with_host(self, host_ip: str) -> None:
        self._socket.connect((host_ip, self._port))

        try:
            msg = self._receive_data()
        except socket.timeout:
            raise NetworkException('No answer from host.')

        if msg['command'] == Command.HELLO:
            self._send_command(Command.HELLO)
        else:
            raise NetworkException('No answer from host.')

        self._logger.info(msg)

    def wait_start_command(self) -> dict:
        self._logger.info('Waiting for start signal.')
        msg = None
        while msg is None:
            try:
                msg = self._encoder.decode(self._socket.recv(1024))
            except socket.timeout:
                self._logger.info('Waiting for start signal.')

        self._logger.info(msg)

        if msg['command'] == Command.START:
            return msg
        else:
            raise NetworkException('Wrong command received.')


