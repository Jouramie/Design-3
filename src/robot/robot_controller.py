import time
from logging import Logger

from src.robot.hardware.command.stm_command_definition import commands_to_stm
from .hardware.channel import Channel
from .hardware.command.command_from_stm import CommandFromStm
from ..d3_network.client_network_controller import ClientNetworkController
from ..d3_network.ip_provider import IpProvider


class RobotController(object):

    def __init__(self, logger: Logger, ip_provider: IpProvider, network: ClientNetworkController, channel: Channel):
        self._logger = logger
        self._ip_provider = ip_provider
        self._network = network
        self._channel = channel

    def start(self) -> None:
        host_ip = self._ip_provider.get_host_ip()

        self._network.pair_with_host(host_ip)

        self._network.wait_start_command()

        self._logger.info("Start command received... LEEETTTS GOOOOOO!! ")
        self._main_loop()

    def receive_country_code(self) -> int:
        return self.receive_command().get_country_code()

    def receive_end_of_task_signal(self) -> CommandFromStm:
        return self.receive_command()

    def receive_command(self):
        msg = None
        while msg is None:
            msg = self._channel.receive_message()
        print(msg)
        return CommandFromStm(bytearray(msg))

    def send_grab_cube(self) -> bool:
        if (self.send_ask_if_can_grab_cube() == True):
            self._channel.send_command(commands_to_stm.Command.GRAB_CUBE.value)
            msg = None
            while msg is None:
                msg = self._channel.receive_message()
                self._logger.info('Received from STM : {}'.format(msg))
            if msg[3:4] == 'fc':
                return True
            else:
                return False

    def send_drop_cube(self) -> None:
        self._channel.send_command(commands_to_stm.Command.DROP_CUBE.value)

    def send_ask_if_can_grab_cube(self) -> bool:
        self._channel.send_command(commands_to_stm.Command.CAN_GRAB_CUBE.value)
        msg = None
        while msg is None:
            msg = self._channel.receive_message()
            self._logger.info('Received from STM : {}'.format(msg))
        if msg[3:4] == 'fc':
            return True
        else:
            return False

    def send_movement_command(self, command: bytearray):
        self._channel.send_command(command)

    def _main_loop(self):
        time.sleep(2)
        # self._network.wait_infrared_ask()
        # self._network.send_infrared_ask(43)

        self.send_grab_cube()
        self.send_drop_cube()

        time.sleep(1000)
