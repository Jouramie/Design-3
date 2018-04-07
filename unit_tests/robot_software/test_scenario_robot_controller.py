from queue import Queue
from unittest import TestCase
from unittest.mock import MagicMock

from src.domain.path_calculator.movement import Forward
from src.robot.robot_controller import RobotController


class TestScenarioRobotController(TestCase):
    def setUp(self):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        ctrl._network_request_queue = Queue()
        ctrl._network_request_queue.put(str(Forward(10)))
    def test_given_robot_controller_when_main_loop_then_treats_network_request(self):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        ctrl._network_request_queue = Queue()
        ctrl._network_request_queue