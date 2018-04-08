from queue import Queue
from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.robot.hardware.command.stm_command_definition import commands_from_stm
from src.robot.robot_controller import RobotController


class TestScenarioRobotController(TestCase):

    def setUp(self):
        network_ctrl = MagicMock()
        network_ctrl.attach_mock(Mock(return_value=None), 'wait_message')
        self.ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())

    def __set_up_scenario_1(self):
        self.ctrl._network_request_queue = Queue()
        self.ctrl._network_request_queue.put({'command': 'move-forward', 'amplitude': 13.0})
        self.ctrl._network_request_queue.put({'command': 'move-right', 'amplitude': 10.0})
        self.ctrl._network_request_queue.put({'command': 'end-signal'})
        self.ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))

    def test_given_robot_controller_when_main_loop_then_treats_network_request(self):
        self.__set_up_scenario_1()
        self.ctrl.main_loop()

        self.assertRaises(IndexError, self.ctrl._stm_commands_todo.pop)
