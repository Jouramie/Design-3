from logging import Logger
from math import sin, cos, pi
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from src.domain.path_calculator.action import Movement, Rotate, Action
from src.vision.robot_detector import MockedRobotDetector
from .command import Command
from .encoder import Encoder
from .network_controller import NetworkController
from .network_exception import NetworkException, WrongCommand


class ServerNetworkController(NetworkController):
    def __init__(self, logger: Logger, port: int, encoder: Encoder):
        super().__init__(logger, port, encoder)

    def host_network(self) -> None:
        raise NotImplementedError("This is an interface...")

    def check_received_infrared_signal(self) -> int:
        raise NotImplementedError("This is an interface...")

    def send_action(self, action: Action) -> None:
        raise NotImplementedError("This is an interface...")

    def send_actions(self, actions: [Action]) -> None:
        raise NotImplementedError("This is an interface...")

    def send_start(self):
        raise NotImplementedError("This is an interface...")

    def check_robot_feedback(self) -> None:
        raise NotImplementedError("This is an interface...")


class SocketServerNetworkController(ServerNetworkController):
    def __init__(self, logger: Logger, port: int, encoder: Encoder):
        super().__init__(logger, port, encoder)
        self._server = socket(AF_INET, SOCK_STREAM)
        self._server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def send_start(self):
        self._send_command(Command.START)

        self._logger.info('Start command sent!')

    def host_network(self) -> None:
        self._logger.info("Creating server on port " + str(self._port))
        self._server.bind(('', self._port))

        while self._socket is None:
            self._server.listen(5)
            self._socket, address = self._server.accept()
            self._socket.settimeout(2)
            self._logger.info("{} connected".format(address))

            self._send_command(Command.HELLO, {'msg': 'ThAnKs YoU fOr CoNnEcTiNg !!!!!'})

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

    def check_robot_feedback(self) -> dict:
        msg = self._receive_message()

        self._logger.info("Feedback from robot : {}".format(msg))

        return msg

    def check_received_infrared_signal(self) -> int:
        msg = self._receive_message()

        country_code = msg['country_code']
        self._logger.info("Infrared signal received! {code}".format(code=country_code))
        return country_code

    def send_action(self, action: Action) -> None:
        if type(action) is Movement:
            self._send_command(Command.ACTION, {'command': action.command, 'amplitude': action.amplitude})
        else:
            self._send_command(Command.ACTION, {'command': action.command})

        self._logger.info("Action sent {}".format(action))

    def send_actions(self, actions: [Action]) -> None:
        actions_command_list = []
        for action in actions:
            actions_command_list.append(action.to_command())
        self._send_command(Command.ACTION, {'actions': actions_command_list})

        self._logger.info("Actions {} sent".format(' ,'.join(str(act.to_command()) for act in actions)))


class MockedServerNetworkController(ServerNetworkController):
    def __init__(self, logger: Logger, country_code: int, port: int = 0,
                 encoder: Encoder = None, robot_detector: MockedRobotDetector = None):
        super().__init__(logger, port, encoder)
        self.MOVEMENT = Rotate(30)
        self.country_code = country_code
        self.has_to_send_country_code = False
        self.robot_detector = robot_detector

    def host_network(self) -> None:
        self._logger.info("Creating server on port " + str(self._port))
        self._logger.info("{} connected".format('fake network'))
        pass

    def send_start(self):
        self._logger.info('Start command sent!')

    def check_received_infrared_signal(self) -> int:
        self._logger.info("Infrared signal received! {code}".format(code=self.country_code))
        return self.country_code

    def send_action(self, action: Action) -> None:
        self._logger.info("Action: {} sent!".format(action))
        self.__update_mock_position(action)

    def send_actions(self, actions: [Action]) -> None:
        for action in actions:
            if action.command == Command.INFRARED_SIGNAL:
                self.has_to_send_country_code = True
            self.__update_mock_position(action)
        self._logger.info("Commands: {} sent!".format(', '.join(str(action) for action in actions)))

    def __update_mock_position(self, action):
        if self.robot_detector is not None:
            if action.command == Command.MOVE_ROTATE:
                self.robot_detector.robot_direction = (self.robot_detector.robot_direction + action.amplitude) % 360
            elif action.command == Command.CAN_I_GRAB:
                pass
            elif action.command == Command.MOVE_FORWARD:
                new_robot_x = self.robot_detector.robot_position[0] + round(
                    cos(self.robot_detector.robot_direction / 360 * 2 * pi), 3) * action.amplitude
                new_robot_y = self.robot_detector.robot_position[1] + round(
                    sin(self.robot_detector.robot_direction / 360 * 2 * pi), 3) * action.amplitude
                self.robot_detector.robot_position = (new_robot_x, new_robot_y)
            elif action.command == Command.MOVE_BACKWARD:
                new_robot_x = self.robot_detector.robot_position[0] - round(
                    cos(self.robot_detector.robot_direction / 360 * 2 * pi), 3) * action.amplitude
                new_robot_y = self.robot_detector.robot_position[1] - round(
                    sin(self.robot_detector.robot_direction / 360 * 2 * pi), 3) * action.amplitude
                self.robot_detector.robot_position = (new_robot_x, new_robot_y)
            elif action.command == Command.MOVE_RIGHT:
                new_robot_x = self.robot_detector.robot_position[0] + round(
                    sin(self.robot_detector.robot_direction / 360 * 2 * pi), 3) * action.amplitude
                new_robot_y = self.robot_detector.robot_position[1] - round(
                    cos(self.robot_detector.robot_direction / 360 * 2 * pi), 3) * action.amplitude
                self.robot_detector.robot_position = (new_robot_x, new_robot_y)
            elif action.command == Command.MOVE_LEFT:
                new_robot_x = self.robot_detector.robot_position[0] - round(
                    sin(self.robot_detector.robot_direction / 360 * 2 * pi), 3) * action.amplitude
                new_robot_y = self.robot_detector.robot_position[1] + round(
                    cos(self.robot_detector.robot_direction / 360 * 2 * pi), 3) * action.amplitude
                self.robot_detector.robot_position = (new_robot_x, new_robot_y)

    def check_robot_feedback(self) -> dict:

        if self.has_to_send_country_code:
            self.has_to_send_country_code = False
            return {'command': Command.INFRARED_SIGNAL, 'country_code': self.country_code}
        else:
            self._logger.info("Feedback from robot: {}".format(Command.EXECUTED_ALL_REQUESTS))
            return {'command': Command.EXECUTED_ALL_REQUESTS}
