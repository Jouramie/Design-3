from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.d3_network.command import Command
from src.robot.hardware.command.stm_command_builder import StmCommand
from src.robot.hardware.command.stm_command_definition import commands_from_stm
from src.robot.robot_controller import RobotController


class TestRobotController(TestCase):
    def test_when_start_controller_then_get_host_ip(self):
        network_scanner = MagicMock()
        ctrl = RobotController(MagicMock(), network_scanner, MagicMock(), MagicMock())

        ctrl._start()

        network_scanner.get_host_ip.assert_called_once()

    def test_given_host_ip_when_start_controller_then_pair_with_host(self):
        host_ip = '10.42.0.78'
        network_scanner = Mock()
        network_scanner.attach_mock(Mock(return_value=host_ip), 'get_host_ip')
        network_ctrl = MagicMock()
        network_ctrl.attach_mock(Mock(return_value=dict({'command': 'end-signal'})), 'wait_message')
        ctrl = RobotController(MagicMock(), network_scanner, network_ctrl, MagicMock())

        ctrl._start()

        network_ctrl.pair_with_host.assert_called_once_with(host_ip)

    def test_when_start_controller_then_wait_start_command(self):
        network_ctrl = MagicMock()
        ctrl = RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())

        ctrl._start()

        network_ctrl.wait_start_command.assert_called_once()

    def test_when_receive_message_from_stm_then_append_it_to_queue(self):
        channel = MagicMock()
        channel.attach_mock(Mock(return_value=commands_from_stm.Feedback(
            commands_from_stm.Message.TASK_RECEIVED_ACK.value)), 'receive_message')
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())

        ctrl.receive_stm_command()

        self.assertEqual(1, ctrl._stm_responses_queue.qsize())

    def test_when_send_movement_command_then_send_via_channel(self):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.receive_message = Mock(return_value=commands_from_stm.Message.SUCCESSFULL_TASK.value)
        ctrl = RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.send_command_to_stm({'command': Command.MOVE_BACKWARD, 'amplitude': 200})

        channel.send_command.assert_called_once_with(bytearray(b'\x3b\x07\xd0'))

    def test_when_add_movement_to_queue_then_movement_added(self):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}

        ctrl.add_stm_command_to_queue(command)

        self.assertEqual(command, ctrl._stm_commands_todo.pop())

    def test_when_treats_network_request_then_adds_it_to_stm_todo_queue(self):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl._network_request_queue.put(command)

        ctrl.treat_network_request()

        self.assertEqual(command, ctrl._stm_commands_todo.pop())

    def test_when_treats_stm_response_task_received_then_add_to_received_queue(self):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl._stm_sent_queue.put(command)
        ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))

        ctrl.treat_stm_response()

        self.assertEqual(command, ctrl._stm_received_queue.get())

    def test_when_treats_stm_response_task_succes_then_add_to_done_queue(self):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl._stm_received_queue.put(command)
        ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))

        ctrl.treat_stm_response()

        self.assertEqual(command, ctrl._stm_done_queue.get())

    def test_when_treats_stm_response_task_failed_then_add_to_todos_to_top_priority(self):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl._stm_received_queue.put(command)
        ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.UNSUCCESSFULL_TASK.value))

        ctrl.treat_stm_response()

        self.assertEqual(command, ctrl._stm_commands_todo.popleft())

    def test_when_treats_stm_response_cube_task_failed_then_notify_server(self):
        network_ctrl = MagicMock()
        ctrl = RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())
        ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.TASK_CUBE_FAILED.value))

        ctrl.treat_stm_response()

        network_ctrl.send_feedback.assert_called_once()

    def test_when_execute_stm_tasks_then_priority_todo_moved_to_sent_queue(self):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl._stm_commands_todo.append(command)

        ctrl.execute_stm_tasks()

        self.assertEqual(command, ctrl._stm_sent_queue.get())

    def test_when_execute_stm_tasks_then_send_via_channel(self):
        channel = MagicMock()
        channel.attach_mock(Mock(), 'send_command')
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), channel)
        ctrl._stm_commands_todo.append(command)

        ctrl.execute_stm_tasks()

        channel.send_command.assert_called_once_with(StmCommand.factory(command))
