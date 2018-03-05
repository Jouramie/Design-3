from logging import Logger
from socket import socket, AF_INET, SOCK_STREAM, timeout

from .command import Command
from .encoder import Encoder
from .network_controller import NetworkController
from .network_exception import NetworkException


class ClientNetworkController(NetworkController):

    def __init__(self, logger: Logger, port: int, encoder: Encoder):
        super().__init__(logger, port, encoder)
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.settimeout(5)

    def pair_with_host(self, host_ip: str) -> None:
        self._socket.connect((host_ip, self._port))

        try:
            msg = self._receive_data()
        except timeout:
            raise NetworkException('No answer from host.')

        if msg['command'] == Command.HELLO:
            self._send_command(Command.HELLO)
        else:
            raise NetworkException('No answer from host.')

        self._logger.info(msg)

    def wait_start_command(self) -> dict:
        self._logger.info('Waiting for start command.')
        msg = None
        while msg is None:
            try:
                msg = self._receive_data()
            except timeout:
                self._logger.info('Waiting for start command.')

        self._logger.info(msg)

        if msg['command'] == Command.START:
            return msg
        else:
            raise NetworkException('Wrong command received.')

    def wait_ir_ask(self) -> dict:
        self._logger.info('Waiting for ir signal.')
        msg = None
        while msg is None:
            try:
                msg = self._receive_data()
            except timeout:
                self._logger.info('Waiting for ir signal.')

        self._logger.info(msg)

        if msg['command'] == Command.IR_SIGNAL:
            return msg
        else:
            raise NetworkException('Wrong command received.')

    def send_ir_ask(self, country_code: int):
        self._logger.info('Sending country_code {}.'.format(country_code))
        self._send_command(Command.IR_SIGNAL, {'country_code': country_code})
