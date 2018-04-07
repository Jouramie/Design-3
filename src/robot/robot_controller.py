import time
from collections import deque
from logging import Logger
from queue import Queue

from .hardware.channel import Channel
from .hardware.command.stm_command_builder import StmCommand
from .hardware.command.stm_command_definition import commands_from_stm
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
        self.task_done = False

    def _start(self) -> None:
        host_ip = self._ip_provider.get_host_ip()
        self._network.pair_with_host(host_ip)
        self._network.wait_start_command()
        self._logger.info("Start command received... LEEETTTS GOOOOOO!! ")

    def receive_stm_command(self):
        msg = self._channel.receive_message()
        while msg.type == commands_from_stm.Feedback.HEY:
            msg = self._channel.receive_message()
        self._stm_responses_queue.put(msg)
        self._logger.info('Received from STM : {}'.format(msg))

    def add_stm_command_to_queue(self, command: dict) -> None:
        if command['command'] in Command.__dict__.values():
            self._stm_commands_todo.append(command)
        else:
            self._logger.info('Received {} from station, but does not know how to execute it, so skipping it'.format(command))

    def send_command_to_stm(self, command: dict) -> None:
        self._channel.send_command(StmCommand.factory(command))

    def treat_network_request(self) -> None:
        if not self._network_request_queue.empty():
            task = self._network_request_queue.get()
            self.add_stm_command_to_queue(task)

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
            elif response.type == commands_from_stm.Feedback.TASK_CUBE_FAILED:
                #stop everything and notify station
                self._stm_commands_todo = deque()
                self._network_request_queue = Queue()
                self._stm_responses_queue = Queue()
                self._stm_received_queue = Queue()
                self._stm_sent_queue = Queue()
                self._stm_done_queue = Queue()
                self._network.send_feedback(Command.GRAB_CUBE_FAILURE)

    def execute_stm_tasks(self) -> None:
        if self._stm_commands_todo:
            task = self._stm_commands_todo.pop()
            self._stm_sent_queue.put(task)
            self.send_command_to_stm(task)

    def main_loop(self) -> None:
        self._start()
        while not self.task_done:
            time.sleep(5)
            self._network_request_queue.put(self._network.wait_message())
            self.treat_network_request()
            self.execute_stm_tasks()
            self.receive_stm_command()
            self.treat_stm_response()
