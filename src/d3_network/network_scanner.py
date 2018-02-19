import nmap


class _NetworkScanner:
    def get_host_ip(self):
        pass


class StaticNetworkScanner(_NetworkScanner):
    def __init__(self, host_ip):
        self._host_ip = host_ip

    def get_host_ip(self):
        return self._host_ip


class NmapNetworkScanner(_NetworkScanner):
    def get_host_ip(self):
        # TODO Scan network using nmap to find host
        return ''
