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
        self.failure = False
        self.waiting_for_commander = True

    def _start(self) -> None:
        host_ip = self._ip_provider.get_host_ip()
        self._network.pair_with_host(host_ip)
        self._network.wait_start_command()
        self._logger.info("Start command received... LEEETTTS GOOOOOO!! ")

    def check_if_all_request_were_executed(self):
        if not self.waiting_for_commander \
                and not self.failure \
                and self._stm_sent_queue.empty() \
                and self._stm_received_queue.empty() \
                and self._network_request_queue.empty() \
                and not self._stm_commands_todo:
            self._network.send_feedback(Command.EXECUTED_ALL_REQUESTS)
            self.waiting_for_commander = True

    def receive_network_request(self):
        network_request = self._network.wait_message()
        self._logger.info(network_request)
        if network_request is not None:
            self.failure = False
            self.waiting_for_commander = False
            self._network_request_queue.put(network_request)

    def receive_stm_command(self):
        msg = self._channel.receive_message()
        if msg is not None and msg.type != commands_from_stm.Feedback.HEY:
            self._stm_responses_queue.put(msg)
        self._logger.info('Received from STM : {}'.format(msg.type))

    def treat_network_request(self) -> None:
        if not self._network_request_queue.empty():
            task = self._network_request_queue.get()
            if task['command'] == 'actions':
                for action in task['actions']:
                    self._add_network_request_to_stm_todo_queue(action)
            else:
                self._add_network_request_to_stm_todo_queue(task)

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
                # stop everything and notify station
                self.failure = True
                self._stm_commands_todo = deque()
                self._network_request_queue = Queue()
                self._stm_responses_queue = Queue()
                self._stm_received_queue = Queue()
                self._network.send_feedback(Command.GRAB_CUBE_FAILURE)

    def execute_next_stm_task_and_check_ACK(self) -> None:
        if self._stm_commands_todo:
            while True:
                self._execute_stm_tasks()
                time.sleep(5)
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

    def _add_network_request_to_stm_todo_queue(self, command: dict) -> None:
        if command['command'] in Command.__dict__.values():
            self._stm_commands_todo.append(command)
        else:
            self._logger.info(
                'Received {} from station, but does not know how to execute it, so skipping it'.format(command))

    def _send_command_to_stm(self, command: dict) -> None:
        if command['command'] == Command.END_SIGNAL:
            self.flag_done = True
        command = StmCommand.factory(command)
        self._logger.info('Sending bytes to STM {:02x} {:02x} {:02x}'.format(command[0], command[1], command[2]))
        self._channel.send_command(command)

    def _execute_stm_tasks(self) -> None:
        if self._stm_commands_todo:
            task = self._stm_commands_todo.popleft()
            self._stm_sent_queue.put(task)
            self._send_command_to_stm(task)

    def main_loop(self) -> None:
        self._start()
        self._logger.info('AAAAAAAAAAAAAAAAAAAAAHHHHHHHHHH')
        while True:
            time.sleep(1)
            self.execute()

            if self.flag_done and self._stm_sent_queue.empty() and self._stm_received_queue.empty():
                return

    def execute(self):
        self.receive_network_request()
        self.treat_network_request()
        self.execute_next_stm_task_and_check_ACK()
        time.sleep(1)
        self.receive_stm_command()
        self.treat_stm_response()
        self.check_if_all_request_were_executed()
