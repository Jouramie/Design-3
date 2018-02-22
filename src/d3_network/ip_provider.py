class _IpProvider:
    def get_host_ip(self):
        pass


class StaticIpProvider(_IpProvider):
    def __init__(self, host_ip):
        self._host_ip = host_ip

    def get_host_ip(self):
        return self._host_ip
