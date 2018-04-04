from logging import Logger
from queue import Queue

from .hardware.channel import Channel
from .hardware.command.command_from_stm import CommandFromStm
from .hardware.command.not_a_country_command_exception import NotACountryCommandException
from .hardware.command.stm_command_definition import commands_from_stm
from .hardware.command.stm_command_definition import commands_to_stm
from ..d3_network.client_network_controller import ClientNetworkController
from ..d3_network.command import Command
from ..d3_network.ip_provider import IpProvider


class RobotController(object):
    def __init__(self, logger: Logger, ip_provider: IpProvider, network: ClientNetworkController, channel: Channel):
        self._logger = logger
        self._ip_provider = ip_provider
        self._network = network
        self._channel = channel
        self._network_queue = Queue()
        self.task_done = False

    def start(self) -> None:
        host_ip = self._ip_provider.get_host_ip()
        self._network.pair_with_host(host_ip)
        self._network.wait_start_command()
        self._logger.info("Start command received... LEEETTTS GOOOOOO!! ")

    def receive_end_of_task_signal(self) -> bool:
        msg = self.receive_command()
        return self._validate_if_successful(msg)

    def receive_command(self):
        msg = None
        while msg is None or msg == "b''" or msg == "b'ff'":
            msg = self._channel.receive_message()
        self._logger.info('Received from STM : {}'.format(msg))
        return CommandFromStm(msg)

    def send_grab_cube(self) -> bool:
        self._channel.send_command(commands_to_stm.Command.GRAB_CUBE.value)
        feedback = self.receive_command()
        return self._validate_if_successful(feedback)

    def send_drop_cube(self) -> bool:
        self._channel.send_command(commands_to_stm.Command.DROP_CUBE.value)
        feedback = self.receive_command()
        return self._validate_if_successful(feedback)

    def send_ask_if_can_grab_cube(self) -> bool:
        self._channel.send_command(commands_to_stm.Command.CAN_GRAB_CUBE.value)
        feedback = self.receive_command()
        return self._validate_if_successful(feedback)

    def send_end_signal(self) -> None:
        self._channel.send_command(commands_to_stm.Command.THE_END.value)
        self.task_done = True

    def send_seek_flag(self) -> None:
        self._channel.send_command(commands_to_stm.Command.SEEK_FLAG.value)

    def send_movement_command(self, command: bytearray) -> None:
        self._channel.send_command(command)

    def _validate_if_successful(self, command: CommandFromStm) -> bool:
        return self._validate_target(command, commands_from_stm.Target.TASK_SUCCESS)

    def _validate_target(self, command: CommandFromStm, target: commands_from_stm.Target) -> bool:
        if command.target == target:
            self._logger.info('Command successfull')
            return True
        else:
            self._logger.info('Command UNsuccessfull')
            return False

    def _execute_flag_sequence(self) -> None:
        command = self.receive_command()
        try:
            self._logger.info('Received country number : {}'.format(command.get_country_code()))
            self._network.send_infrared_ask(command.get_country_code())
        except NotACountryCommandException:
            self._logger.info('Expected a country number but received : {}'.format(command.command))

    def execute(self) -> None:
        if not self._network_queue.empty():
            msg = self._network_queue.get()
            self._logger.info('Executing this command : {}'.format(msg))
            if msg['command'] == Command.INFRARED_SIGNAL:
                self.send_seek_flag()
                self._execute_flag_sequence()
            elif msg['command'] == Command.CAN_I_GRAB:
                self.send_ask_if_can_grab_cube()
            elif msg['command'] == Command.GRAB:
                self.send_grab_cube()
            elif msg['command'] == Command.DROP:
                self.send_drop_cube()
            elif msg['command'] == Command.END_SIGNAL:
                self.send_end_signal()
            elif msg['command'] == Command.MOVE:
                self.send_movement_command(msg['msg'])
            else:
                self._logger.info('Received this {} but does not know how to deal with it'.format(msg))
                raise NotImplementedError("Please do more stuff")

    def _main_loop(self) -> None:
        self.start()
        while not self.task_done:
            self._network_queue.put(self._network.wait_message())
            self.execute()
