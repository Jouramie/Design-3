class RobotController:

    def __init__(self, logger, network_scanner, network):
        self._logger = logger
        self._network_scanner = network_scanner
        self._network = network

    def start(self):
        host_ip = self._network_scanner.get_host_ip()
        self._network.pair_with_host(host_ip)

        self._network.wait_start_command(self.on_receive_start_command)

    def on_receive_start_command(self):
        self._logger.info("Start command received... LEEETTTS GOOOOOO!! ")
        self._main_loop()

    def _main_loop(self):
        pass


