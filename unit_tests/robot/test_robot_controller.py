from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from src.d3_network.command import Command
from src.robot.hardware.command.stm_command_definition import commands_from_stm
from src.robot.hardware.command.stm_command_factory import StmCommand
from src.robot.robot_controller import RobotController


class TestRobotController(TestCase):
    @patch('src.robot.robot_controller.time')
    def test_when_start_controller_then_get_host_ip(self, time):
        network_scanner = MagicMock()
        ctrl = RobotController(MagicMock(), network_scanner, MagicMock(), MagicMock())

        ctrl._start()

        network_scanner.get_host_ip.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_given_host_ip_when_start_controller_then_pair_with_host(self, time):
        host_ip = '10.42.0.78'
        network_scanner = Mock()
        network_scanner.attach_mock(Mock(return_value=host_ip), 'get_host_ip')
        network_ctrl = MagicMock()
        network_ctrl.attach_mock(Mock(return_value=dict({'command': 'end-signal'})), 'wait_message')
        ctrl = RobotController(MagicMock(), network_scanner, network_ctrl, MagicMock())

        ctrl._start()

        network_ctrl.pair_with_host.assert_called_once_with(host_ip)

    @patch('src.robot.robot_controller.time')
    def test_when_start_controller_then_wait_start_command(self, time):
        network_ctrl = MagicMock()
        ctrl = RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())

        ctrl._start()

        network_ctrl.wait_start_command.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_when_check_if_all_request_were_executed_then_notifies_network_if_so(self, time):
        network_ctrl = MagicMock()
        ctrl = RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())

        ctrl.check_if_all_request_were_executed()

        network_ctrl.send_feedback.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_when_check_if_all_request_were_executed_then_does_not_notify_when_todo_queue_full(self, time):
        network_ctrl = MagicMock()
        ctrl = RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())
        ctrl._stm_commands_todo.append({'command': Command.GRAB})

        ctrl.check_if_all_request_were_executed()

        self.assertEqual(0, network_ctrl.called)

    @patch('src.robot.robot_controller.time')
    def test_when_receive_network_request_then_fills_net_work_request_queue(self, time):
        network_ctrl = MagicMock()
        command = {'command': Command.CAN_I_GRAB}
        network_ctrl.attach_mock(Mock(return_value=command), 'wait_message')
        ctrl = RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())

        ctrl.receive_network_request()

        self.assertEqual(command, ctrl._network_request_queue.get())

    @patch('src.robot.robot_controller.time')
    def test_when_receive_message_from_stm_then_append_it_to_queue(self, time):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())

        ctrl.receive_stm_command()

        self.assertEqual(1, ctrl._stm_responses_queue.qsize())

    @patch('src.robot.robot_controller.time')
    def test_when_receive_message_from_stm_then_receive_from_channel(self, time):
        channel = MagicMock()
        channel.attach_mock(Mock(return_value=commands_from_stm.Feedback(
            commands_from_stm.Message.TASK_RECEIVED_ACK.value)), 'receive_message')
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), channel)

        ctrl.receive_stm_command()

        channel.receive_message.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_when_send_movement_command_then_send_via_channel(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.receive_message = Mock(return_value=commands_from_stm.Message.SUCCESSFULL_TASK.value)
        ctrl = RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl._send_command_to_stm({'command': Command.MOVE_BACKWARD, 'amplitude': 200})

        channel.send_command.assert_called_once_with(bytearray(b'\x3b\x07\xd0'))

    @patch('src.robot.robot_controller.time')
    def test_when_send_ir_signal_command_then_set_flag_done(self, time):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())

        ctrl._send_command_to_stm({'command': Command.END_SIGNAL})

        self.assertEqual(True, ctrl.flag_done)

    @patch('src.robot.robot_controller.time')
    def test_when_add_movement_to_queue_then_movement_added(self, time):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}

        ctrl._add_network_request_to_stm_todo_queue(command)

        self.assertEqual(command, ctrl._stm_commands_todo.pop())

    @patch('src.robot.robot_controller.time')
    def test_when_treats_network_request_then_adds_it_to_stm_todo_queue(self, time):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl._network_request_queue.put(command)

        ctrl.treat_network_request()

        self.assertEqual(command, ctrl._stm_commands_todo.pop())

    @patch('src.robot.robot_controller.time')
    def test_when_treats_stm_response_task_received_then_add_to_received_queue(self, time):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl._stm_sent_queue.put(command)
        ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.TASK_RECEIVED_ACK.value))

        ctrl.treat_stm_response()

        self.assertEqual(command, ctrl._stm_received_queue.get())

    @patch('src.robot.robot_controller.time')
    def test_when_treats_stm_response_task_succes_then_add_to_done_queue(self, time):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl._stm_received_queue.put(command)
        ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.SUCCESSFULL_TASK.value))

        ctrl.treat_stm_response()

        self.assertEqual(command, ctrl._stm_done_queue.get())

    @patch('src.robot.robot_controller.time')
    def test_when_treats_stm_response_task_failed_then_add_to_todos_to_top_priority(self, time):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl._stm_received_queue.put(command)
        ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.UNSUCCESSFULL_TASK.value))

        ctrl.treat_stm_response()

        self.assertEqual(command, ctrl._stm_commands_todo.popleft())

    @patch('src.robot.robot_controller.time')
    def test_when_treats_stm_response_cube_task_failed_then_notify_server(self, time):
        network_ctrl = MagicMock()
        ctrl = RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())
        command = {'command': Command.GRAB}
        ctrl._stm_received_queue.put(command)
        ctrl._stm_responses_queue.put(commands_from_stm.Feedback(commands_from_stm.Message.TASK_CUBE_FAILED.value))

        ctrl.treat_stm_response()

        network_ctrl.send_feedback.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_when_treats_stm_response_country_code_then_notify_server(self, time):
        network_ctrl = MagicMock()
        ctrl = RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())
        ctrl._stm_responses_queue.put(commands_from_stm.Feedback(bytearray(b'\xb0\x75\x00\x00')))
        command = {'command': Command.GRAB}
        ctrl._stm_received_queue.put(command)

        ctrl.treat_stm_response()

        network_ctrl.send_country_code.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_when_execute_stm_tasks_then_priority_todo_moved_to_sent_queue(self, time):
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), MagicMock())
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl._stm_commands_todo.append(command)

        ctrl._execute_stm_tasks()

        self.assertEqual(command, ctrl._stm_sent_queue.get())

    @patch('src.robot.robot_controller.time')
    def test_when_execute_stm_tasks_then_send_via_channel(self, time):
        channel = MagicMock()
        channel.attach_mock(Mock(), 'send_command')
        command = {'command': Command.MOVE_FORWARD, 'amplitude': 2222}
        ctrl = RobotController(MagicMock(), MagicMock(), MagicMock(), channel)
        ctrl._stm_commands_todo.append(command)

        ctrl._execute_stm_tasks()

        channel.send_command.assert_called_once_with(StmCommand.factory(command))
