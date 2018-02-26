from src.robot_software import robot_controller

import pytest
from unittest.mock import MagicMock
from unittest.mock import call


def test_network():
    network = MagicMock()
    ctrl = robot_controller.RobotController(network)

    ctrl.start()

    assert network.method_calls == [call.pair_with_host()]
