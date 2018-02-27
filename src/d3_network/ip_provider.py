class IpProvider(object):
    def get_host_ip(self):
        pass


class StaticIpProvider(IpProvider):
    def __init__(self, host_ip: str):
        self._host_ip = host_ip

    def get_host_ip(self) -> str:
        return self._host_ip
