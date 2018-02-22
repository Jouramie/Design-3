class RobotController:

    def __init__(self, network_scanner, network):
        self.network_scanner = network_scanner
        self.network = network

    def start(self):
        host_ip = self.network_scanner.get_host_ip()
        self.network.pair_with_host(host_ip)

        self.network.wait_start_command(self.on_receive_main_signal)

    def on_receive_main_signal(self):
        self._main_loop()

    def _main_loop(self):
        pass


