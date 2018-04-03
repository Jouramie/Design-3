from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from src.robot import robot_controller
from src.robot.hardware.command.stm_command_builder import StmCommandBuilder
from src.robot.hardware.command.not_a_country_command_exception import NotACountryCommandException
from src.robot.hardware.command.stm_command_definition import commands_to_stm, commands_from_stm


class TestRobotController(TestCase):

    @patch('src.robot.robot_controller.time')
    def test_when_start_controller_then_get_host_ip(self, time):
        network_scanner = MagicMock()
        ctrl = robot_controller.RobotController(MagicMock(), network_scanner, MagicMock(), MagicMock())

        ctrl.start()

        network_scanner.get_host_ip.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_given_host_ip_when_start_controller_then_pair_with_host(self, time):
        host_ip = '10.42.0.78'
        network_scanner = Mock()
        network_scanner.attach_mock(Mock(return_value=host_ip), 'get_host_ip')
        network_ctrl = MagicMock()
        ctrl = robot_controller.RobotController(MagicMock(), network_scanner, network_ctrl, MagicMock())

        ctrl.start()

        network_ctrl.pair_with_host.assert_called_once_with(host_ip)

    @patch('src.robot.robot_controller.time')
    def test_when_start_controller_then_wait_start_command(self, time):
        network_ctrl = MagicMock()
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, MagicMock())

        ctrl.start()

        network_ctrl.wait_start_command.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_when_receive_country_code_then_return_country_code(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.receive_message = Mock(return_value="b'\xb0\x43\x12\xfb'")
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.receive_country_code()

        channel.receive_message.assert_called_once()

    @patch('src.robot.robot_controller.time')
    def test_when_receive_wrong_country_code_then_raise_not_a_country_command_exception(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.receive_message = Mock(return_value="b'\xb1\x43\x12\xfa'")
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        self.assertRaises(NotACountryCommandException, ctrl.receive_country_code)


    @patch('src.robot.robot_controller.time')
    def test_when_send_grab_cube_then_send_via_channel(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.send_command = Mock()
        channel.receive_message = Mock(return_value="b'\xfc\x12\x34\xbe'")
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)
        ctrl.send_ask_if_can_grab_cube = Mock(return_value=True)

        ctrl.send_grab_cube()

        channel.send_command.assert_called_once_with(commands_to_stm.Command.GRAB_CUBE.value)

    @patch('src.robot.robot_controller.time')
    def test_when_send_grab_cube_and_not_ready_then_return_false(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.send_command = Mock()
        channel.receive_message = Mock(return_value="b'\xfc\x12\x34\xbe'")
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)
        ctrl.send_ask_if_can_grab_cube = Mock(return_value=False)

        ctrl.send_grab_cube()

        self.assertEqual(False, ctrl.send_grab_cube())

    @patch('src.robot.robot_controller.time')
    def test_when_send_drop_cube_then_send_via_channel(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.send_command = Mock()
        channel.receive_message = Mock(return_value=commands_from_stm.Command.END_OF_TASK.value)
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.send_drop_cube()

        channel.send_command.assert_called_once_with(commands_to_stm.Command.DROP_CUBE.value)

    @patch('src.robot.robot_controller.time')
    def test_when_ask_if_can_grab_cube_then_send_via_channel(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.send_command = Mock()
        channel.receive_message = Mock(return_value=commands_from_stm.Command.END_OF_TASK.value)
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.send_ask_if_can_grab_cube()

        channel.send_command.assert_called_once_with(commands_to_stm.Command.CAN_GRAB_CUBE.value)

    @patch('src.robot.robot_controller.time')
    def test_when_send_movement_command_then_send_via_channel(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.send_command = Mock()
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.send_movement_command(StmCommandBuilder().forward(5))

        channel.send_command.assert_called_once_with(bytearray(b'\x33\x05\xff'))

    @patch('src.robot.robot_controller.time')
    def test_when_receive_successful_end_of_task_then_message_received_correclty(self, time):
        network_ctrl = MagicMock()
        channel = Mock()
        channel.receive_message = Mock(return_value="b'\xfc\x12\x34\xbe'")
        ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)

        ctrl.receive_end_of_task_signal()

        channel.receive_message.assert_called_once()

    # @patch('src.robot.robot_controller.time')
    # def test_robot(self, time):
    #     network_ctrl = MagicMock()
    #     channel = create_channel('/dev/ttyUSB0')
    #     ctrl = robot_controller.RobotController(MagicMock(), MagicMock(), network_ctrl, channel)
    #
    #     ctrl._main_loop()
