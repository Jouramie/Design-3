from queue import Queue
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from src.d3_network.command import Command
from src.robot.hardware.command.stm_command_definition import commands_from_stm
from src.robot.robot_controller import RobotController


class TestScenarioRobotController(TestCase):

    def setUp(self):
        network_ctrl = MagicMock()
        network_ctrl.attach_mock(Mock(return_value=None), 'wait_message')
        self.ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())

    def test_scenario_1_easy_going(self):
        self.__set_up_scenario_1()
        self.ctrl.main_loop()

        self.assertEqual(3, self.ctrl._stm_done_queue.qsize())
        self.assertEqual(1, self.ctrl._stm_sent_queue.empty())
        self.assertRaises(IndexError, self.ctrl._stm_commands_todo.pop)

    def test_scenario_2_task_failure(self):
        self.__set_up_scenario_1()
        self.ctrl.main_loop()

        self.assertEqual(3, self.ctrl._stm_done_queue.qsize())
        self.assertEqual(1, self.ctrl._stm_sent_queue.empty())
        self.assertRaises(IndexError, self.ctrl._stm_commands_todo.pop)

    def test_scenario_3_ir_signal(self):
        self.__set_up_scenario_3()
        self.ctrl.main_loop()

        self.assertEqual(4, self.ctrl._stm_done_queue.qsize())
        self.assertTrue(self.ctrl._stm_sent_queue.empty())
        self.assertRaises(IndexError, self.ctrl._stm_commands_todo.pop)

    def test_scenario_4_many_moves_and_ir(self):
        self.__set_up_scenario_4()

        self.ctrl.main_loop()

        self.assertTrue(self.ctrl._stm_sent_queue.empty())
        self.assertRaises(IndexError, self.ctrl._stm_commands_todo.pop)
        self.assertEqual(5, self.ctrl._stm_done_queue.qsize())

    def test_scenario_5_no_ack_but_success(self):
        self.__set_up_scenario_5()

        self.ctrl.main_loop()

        self.assertTrue(self.ctrl._stm_sent_queue.empty())
        self.assertRaises(IndexError, self.ctrl._stm_commands_todo.pop)
        self.assertEqual(3, self.ctrl._stm_done_queue.qsize())

    def test_scenario_6_no_ack_but_failed(self):
        self.__set_up_scenario_6()

        self.ctrl.main_loop()

        self.assertTrue(self.ctrl._stm_sent_queue.empty())
        self.assertRaises(IndexError, self.ctrl._stm_commands_todo.pop)
        self.assertEqual(3, self.ctrl._stm_done_queue.qsize())

    def __set_up_scenario_1(self):
        self.ctrl._network_request_queue = Queue()
        self.ctrl._network_request_queue.put({'command': 'move-forward', 'amplitude': 13.0})
        self.ctrl._network_request_queue.put({'command': 'move-right', 'amplitude': 10.0})
        self.ctrl._network_request_queue.put({'command': 'end-signal'})
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))

    def __set_up_scenario_2(self):
        self.ctrl._network_request_queue = Queue()
        self.ctrl._network_request_queue.put({'command': 'move-forward', 'amplitude': 13.0})
        self.ctrl._network_request_queue.put({'command': 'move-right', 'amplitude': 10.0})
        self.ctrl._network_request_queue.put({'command': 'end-signal'})
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.UNSUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))

    def __set_up_scenario_3(self):
        self.ctrl._network_request_queue = Queue()
        self.ctrl._network_request_queue.put({'command': Command.MOVE_FORWARD, 'amplitude': 13.0})
        self.ctrl._network_request_queue.put({'command': Command.MOVE_RIGHT, 'amplitude': 10.0})
        self.ctrl._network_request_queue.put({'command': Command.INFRARED_SIGNAL})
        self.ctrl._network_request_queue.put({'command': 'end-signal'})
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(commands_from_stm.Feedback(bytearray(b'\xb0\x75\x12\xc9')))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))

    def __set_up_scenario_4(self):
        self.ctrl._network_request_queue = Queue()
        self.ctrl._network_request_queue.put({'command': Command.ACTION, 'actions': [
            {'command': Command.MOVE_BACKWARD, 'amplitude': 18},
            {'command': Command.MOVE_FORWARD, 'amplitude': 90},
            {'command': Command.MOVE_LEFT, 'amplitude': 30}]})
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl.execute()
        self.ctrl._network_request_queue.put({'command': Command.INFRARED_SIGNAL})
        self.ctrl._network_request_queue.put({'command': 'end-signal'})
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(commands_from_stm.Feedback(bytearray(b'\xb0\x75\x12\xc9')))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))

    def __set_up_scenario_5(self):
        self.ctrl._network_request_queue = Queue()
        self.ctrl._network_request_queue.put({'command': Command.ACTION, 'actions': [
            {'command': Command.MOVE_BACKWARD, 'amplitude': 18},
            {'command': Command.MOVE_BACKWARD, 'amplitude': 18}]})
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl.execute()
        self.ctrl._network_request_queue.put({'command': 'end-signal'})
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))

    def __set_up_scenario_6(self):
        self.ctrl._network_request_queue = Queue()
        self.ctrl._network_request_queue.put({'command': Command.ACTION, 'actions': [
            {'command': Command.MOVE_BACKWARD, 'amplitude': 18},
            {'command': Command.MOVE_BACKWARD, 'amplitude': 18}]})
        self.ctrl._network_request_queue.put({'command': 'end-signal'})
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.UNSUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))
        self.ctrl._stm_responses_deque.append(
            commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))
