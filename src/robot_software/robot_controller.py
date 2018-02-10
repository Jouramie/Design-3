class RobotController:

    def __init__(self, network):
        self.network = network

    def start(self):
        self.network.pair_with_host()

