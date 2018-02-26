from unittest import TestCase

from src.d3_network import ip_provider


class TestCamera(TestCase):

    def test_given_host_ip_when_create_static_ip_provider_then_get_host_ip_return_host_ip(self):
        static_host_ip = '10.42.0.78'

        scanner = ip_provider.StaticIpProvider(static_host_ip)

        self.assertEqual(scanner.get_host_ip(), static_host_ip)
