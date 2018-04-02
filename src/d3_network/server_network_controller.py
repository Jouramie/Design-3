from logging import Logger
from socket import socket, AF_INET, SOCK_STREAM

from .command import Command
from .encoder import Encoder
from .network_controller import NetworkController
from .network_exception import NetworkException, WrongCommand


class ServerNetworkController(NetworkController):

    def __init__(self, logger: Logger, port: int, encoder: Encoder):
        super().__init__(logger, port, encoder)
        self._server = socket(AF_INET, SOCK_STREAM)

    def host_network(self) -> None:
        self._logger.info("Creating server on port " + str(self._port))
        self._server.bind(('', self._port))

        while self._socket is None:
            self._server.listen(5)
            self._socket, address = self._server.accept()
            self._socket.settimeout(2)
            self._logger.info("{} connected".format(address))

            self._send_command(Command.HELLO, {'msg': "ThAnKs YoU fOr CoNnEcTiNg !!!!1"})

            try:
                msg = self._receive_message()
            except socket.timeout:
                self._socket.close()
                raise NetworkException('No answer from client.')

            if msg['command'] != Command.HELLO:
                self._socket.close()
                raise WrongCommand(Command.HELLO, msg['command'])

            self._logger.info(msg)
        self._socket.setblocking(0)

    def send_start_command(self) -> None:
        self._send_command(Command.START)

        self._logger.info("Start command sent!")

    def send_reset_command(self) -> None:
        self._send_command(Command.RESET)

        self._logger.info("Reset command sent!")

    def ask_infrared_signal(self) -> None:
        self._send_command(Command.INFRARED_SIGNAL)

        self._logger.info("Infrared signal asked!")

    def check_infrared_signal(self) -> int:
        msg = self._receive_message()

        country_code = msg['country_code']
        self._logger.info("Infrared signal received! {code}".format(code=country_code))
        return country_code
