from logging import Logger
from socket import socket, AF_INET, SOCK_STREAM, timeout
from time import sleep

from .command import Command
from .encoder import Encoder
from .network_controller import NetworkController
from .network_exception import NetworkException, WrongCommand, MessageNotReceivedYet


class ClientNetworkController(NetworkController):
    def __init__(self, logger: Logger, port: int, encoder: Encoder):
        super().__init__(logger, port, encoder)
        self._socket = socket(AF_INET, SOCK_STREAM)
        self._socket.settimeout(2)

    def pair_with_host(self, host_ip: str) -> None:
        self._socket.connect((host_ip, self._port))

        try:
            msg = self._receive_message()
        except timeout:
            raise NetworkException('No answer from host.')

        if msg['command'] == Command.HELLO:
            self._send_command(Command.HELLO)
        else:
            raise WrongCommand(Command.HELLO, msg['command'])

        self._logger.info(msg)
        self._socket.setblocking(0)

    def wait_start_command(self) -> dict:
        self._logger.info('Waiting for start command.')
        msg = None
        while msg is None:
            try:
                msg = self._receive_message()
            except MessageNotReceivedYet:
                self._logger.info('Waiting for start command.')
                sleep(1)

        self._logger.info(msg)

        if msg['command'] == Command.START:
            return msg
        else:
            raise WrongCommand(Command.START, msg['command'])

    def wait_infrared_ask(self) -> dict:
        self._logger.info('Waiting for infrared signal.')
        msg = None
        while msg is None:
            try:
                msg = self._receive_message()
            except MessageNotReceivedYet:
                self._logger.info('Waiting for infrared signal.')
                sleep(1)

        self._logger.info(msg)

        if msg['command'] == Command.INFRARED_SIGNAL:
            return msg
        else:
            raise WrongCommand(Command.INFRARED_SIGNAL, msg['command'])

    def send_infrared_ask(self, country_code: int) -> None:
        self._logger.info('Sending country_code {code}.'.format(code=country_code))
        self._send_command(Command.INFRARED_SIGNAL, {'country_code': country_code})

    def wait_message(self) -> dict:
        self._logger.info('Waiting for a command.')
        msg = None
        while msg is None:
            try:
                msg = self._receive_message()
            except MessageNotReceivedYet:
                self._logger.info('Waiting for a command.')
        self._logger.info(msg)
        return msg
