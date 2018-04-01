import time
from logging import Logger

from .hardware.command.command import CommandFromStm
from .hardware.command.stm_command import CommandsToStm, CommandsFromStm
from ..d3_network.client_network_controller import ClientNetworkController
from ..d3_network.ip_provider import IpProvider
from .hardware.channel import Channel


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
        return self._receive_command(CommandsFromStm.PAYS).get_country_code()

    def receive_final_signal(self) -> CommandFromStm:
        return self._receive_command(CommandsFromStm.FIN_TACHE)

    def _receive_command(self, target: CommandsFromStm):
        msg = None
        while msg is None:
            msg = self._channel.receive_message()

        command = CommandFromStm(bytearray(msg))
        if command.target == target.value:
            return command
        else:
            self._receive_command(target)

    def send_grab_cube(self) -> None:
        self._channel.send_command(CommandsToStm.GRAB_CUBE.value)

    def send_drop_cube(self) -> None:
        self._channel.send_command(CommandsToStm.DROP_CUBE.value)

    def ask_if_can_grab_cube(self) -> None:
        self._channel.send_command(CommandsToStm.CAN_GRAB_CUBE.value)

    def _main_loop(self):
        time.sleep(2)
        # self._network.wait_infrared_ask()
        # self._network.send_infrared_ask(43)

        self.send_grab_cube()
        time.sleep(10)
        self.send_drop_cube()

        time.sleep(1000)
