import time
from collections import deque
from logging import Logger
from queue import Queue

from .hardware.channel import Channel
from .hardware.command.stm_command_definition import commands_from_stm
from .hardware.command.stm_command_factory import StmCommand
from ..d3_network.client_network_controller import ClientNetworkController
from ..d3_network.command import Command
from ..d3_network.ip_provider import IpProvider


class RobotController(object):
    def __init__(self, logger: Logger, ip_provider: IpProvider, network: ClientNetworkController, channel: Channel):
        self._logger = logger
        self._ip_provider = ip_provider
        self._network = network
        self._channel = channel
        self._stm_commands_todo = deque()
        self._network_request_queue = Queue()
        self._stm_responses_queue = Queue()
        self._stm_received_queue = Queue()
        self._stm_sent_queue = Queue()
        self._stm_done_queue = Queue()
        self.flag_done = False

    def _start(self) -> None:
        host_ip = self._ip_provider.get_host_ip()
        self._network.pair_with_host(host_ip)
        self._network.wait_start_command()
        self._logger.info("Start command received... LEEETTTS GOOOOOO!! ")

    def receive_stm_command(self):
        msg = self._channel.receive_message()
        while msg.type == commands_from_stm.Feedback.HEY:
            try:
                self._logger.info('Crap from STM : {}'.format(msg.message))
            except Exception:
                self._logger.info('Crap from STM : {}'.format(msg))
            msg = self._channel.receive_message()
        if msg is not None: self._stm_responses_queue.put(msg)
        self._logger.info('Received from STM : {}'.format(msg.type))

    def add_network_request_to_stm_todo_queue(self, command: dict) -> None:
        if command['command'] in Command.__dict__.values():
            self._stm_commands_todo.append(command)
        else:
            self._logger.info('Received {} from station, but does not know how to execute it, so skipping it'.format(command))

    def send_command_to_stm(self, command: dict) -> None:
        command1 = StmCommand.factory(command)
        self._logger.info('Sending to STM {:02x} {:02x} {:02x}'.format(command1[0], command1[1], command1[2]))
        self._channel.send_command(command1)
        if command['command'] == Command.END_SIGNAL:
            self.flag_done = True

    def treat_network_request(self) -> None:
        if not self._network_request_queue.empty():
            task = self._network_request_queue.get()
            self.add_network_request_to_stm_todo_queue(task)

    def treat_stm_response(self) -> None:
        if not self._stm_responses_queue.empty():
            response = self._stm_responses_queue.get()
            if response.type == commands_from_stm.Feedback.TASK_RECEIVED:
                task = self._stm_sent_queue.get()
                self._stm_received_queue.put(task)
            elif response.type == commands_from_stm.Feedback.TASK_SUCCESS:
                task = self._stm_received_queue.get()
                self._stm_done_queue.put(task)
            elif response.type == commands_from_stm.Feedback.TASK_FAILED:
                task = self._stm_received_queue.get()
                self._stm_commands_todo.appendleft(task)
            elif response.type == commands_from_stm.Feedback.COUNTRY:
                task = self._stm_received_queue.get()
                self._stm_done_queue.put(task)
                self._network.send_country_code(response.country)
            elif response.type == commands_from_stm.Feedback.TASK_CUBE_FAILED:
                #stop everything and notify station
                self._stm_commands_todo = deque()
                self._network_request_queue = Queue()
                self._stm_responses_queue = Queue()
                self._stm_received_queue = Queue()
                self._network.send_feedback(Command.GRAB_CUBE_FAILURE)

    def execute_and_check_ACK(self) -> None:
        while True:
            self.execute_stm_tasks()
            time.sleep(2)
            self.receive_stm_command()
            if not self._stm_responses_queue.empty():
                response = self._stm_responses_queue.get()
                if response.type == commands_from_stm.Feedback.TASK_RECEIVED:
                    task = self._stm_sent_queue.get()
                    self._stm_received_queue.put(task)
                    return
                else:
                    task = self._stm_sent_queue.get()
                    self._stm_commands_todo.appendleft(task)

    def execute_stm_tasks(self) -> None:
        if self._stm_commands_todo:
            task = self._stm_commands_todo.pop()
            self._stm_sent_queue.put(task)
            self.send_command_to_stm(task)

    def main_loop(self) -> None:
        self._start()
        while True:
            time.sleep(1)
            network_request = self._network.wait_message()
            if network_request is not None:
                self._network_request_queue.put(network_request)
            self.treat_network_request()
            self.execute_and_check_ACK()
            self.receive_stm_command()
            self.treat_stm_response()

            if self.flag_done and self._stm_sent_queue.empty() and self._stm_received_queue.empty():
                return

