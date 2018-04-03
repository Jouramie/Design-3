import time
from logging import Logger

from .hardware.command.stm_command_definition import commands_from_stm
from .hardware.command.stm_command_definition import commands_to_stm
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


    def receive_end_of_task_signal(self) -> bool:
        msg = self.receive_command()
        return self._validate_target(msg, commands_from_stm.Target.TASK_SUCCESS)

    def receive_command(self):
        msg = None
        while msg is None:
            msg = self._channel.receive_message()
            self._logger.info('Received from STM : {}'.format(msg))
        return CommandFromStm(msg)

    def send_grab_cube(self) -> bool:
        if (self.send_ask_if_can_grab_cube() == True):
            self._channel.send_command(commands_to_stm.Command.GRAB_CUBE.value)
            feedback = self.receive_command()
            return self._validate_if_successful(feedback)
        else:
            return False

    def send_drop_cube(self) -> bool:
        self._channel.send_command(commands_to_stm.Command.DROP_CUBE.value)
        feedback = self.receive_command()
        return self._validate_if_successful(feedback)

    def send_ask_if_can_grab_cube(self) -> bool:
        self._channel.send_command(commands_to_stm.Command.CAN_GRAB_CUBE.value)
        feedback = self.receive_command()
        return self._validate_if_successful(feedback)

    def send_end_signal(self):
        self._channel.send_command(commands_to_stm.Command.THE_END.value)

    def send_seek_flag(self):
        self._channel.send_command(commands_to_stm.Command.SEEK_FLAG.value)

    def send_movement_command(self, command: bytearray):
        self._channel.send_command(command)

    def _validate_if_successful(self, command: CommandFromStm) -> bool:
        return self._validate_target(command, commands_from_stm.Target.TASK_SUCCESS)

    def _validate_target(self, command: CommandFromStm, target: commands_from_stm.Target) -> bool:
        if command.target == target:
            return True
        else:
            return False

    def _main_loop(self):
        time.sleep(2)
        # self._network.wait_infrared_ask()
        # self._network.send_infrared_ask(43)
        self.send_seek_flag()
        # self.receive_country_code()

        self.send_end_signal()

        time.sleep(1000)

