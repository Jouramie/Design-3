import time
from logging import Logger

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

    def _main_loop(self):
        time.sleep(2)
        self._network.wait_infrared_ask()
        self._network.send_infrared_ask(43)

        time.sleep(1000)

