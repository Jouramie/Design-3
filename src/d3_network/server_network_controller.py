import socket
from logging import Logger

from .command import Command
from .encoder import Encoder
from .network_controller import NetworkController
from .network_exception import NetworkException


class ServerNetworkController(NetworkController):

    def __init__(self, logger: Logger, port: int, encoder: Encoder):
        super().__init__(logger, port, encoder)
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def host_network(self) -> None:
        self._server.bind(('', self._port))

        while self._socket is None:
            self._server.listen(5)
            self._socket, address = self._server.accept()
            self._socket.settimeout(10)
            self._logger.info("{} connected".format(address))

            self._send_command(Command.HELLO, {'msg': "ThAnKs YoU fOr CoNnEcTiNg !!!!1"})

            try:
                msg = self._receive_data()
            except socket.timeout:
                self._socket.close()
                raise NetworkException('No answer from client.')

            if msg['command'] != Command.HELLO:
                self._socket.close()
                raise NetworkException('No answer from client.')

            self._logger.info(msg)

    def send_start_command(self) -> None:
        msg = {'command': Command.START}
        self._socket.send(self._encoder.encode(msg))

        self._logger.info("Start command sent!")

    def send_reset_command(self) -> None:
        msg = {'command': Command.RESET}
        self._socket.send(self._encoder.encode(msg))

        self._logger.info("Reset command sent!")

    def ask_ir_signal(self) -> None:
        msg = {'command': Command.IR_SIGNAL}
        self._socket.send(self._encoder.encode(msg))
        self._socket.settimeout(1)

        self._logger.info("Infrared signal asked command sent!")

    def check_ir_signal(self) -> int:
        try:
            encoded_message = self._socket.recv(1024)
            print(encoded_message)
            msg = self._encoder.decode(encoded_message)
            country_code = msg['country_code']
            self._logger.info("Infrared signal received! {}".format(country_code))
            return country_code
        except socket.timeout:
            self._logger.info("No infrared signal received!")
            return 0

