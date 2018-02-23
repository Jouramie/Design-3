class RobotController:

    def __init__(self, network_scanner, network):
        self.network_scanner = network_scanner
        self.network = network

    def start(self):
        host_ip = self.network_scanner.get_host_ip()
        self.network.pair_with_host(host_ip)

