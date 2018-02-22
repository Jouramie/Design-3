from src.d3_network import network_scanner


def test_given_static_host_ip_when_create_static_network_scanner_then_get_host_ip_return_host_ip():
    static_host_ip = '10.42.0.78'

    scanner = network_scanner.StaticIpProvider(static_host_ip)

    assert scanner.get_host_ip() == static_host_ip
