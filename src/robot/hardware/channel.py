from logging import Logger
from time import sleep

import serial

from .channel_exception import ChannelException
from .command.stm_command_definition import commands_from_stm


class Channel(object):
    def __init__(self, serial: serial.Serial, logger: Logger):
        self.serial = serial
        self._logger = logger

    def receive_message(self) -> commands_from_stm.Feedback:
        if self.serial.is_open:
            try:
                msg = bytearray(self.serial.read(commands_from_stm.Message.BYTES_TO_READ.value))
                self._logger.info(
                    'Channel received : {:02x} {:02x} {:02x} {:02x}'.format(msg[0], msg[1], msg[2], msg[3]))
                return commands_from_stm.Feedback(msg)
            except Exception:
                pass
        else:
            raise ChannelException('Serial connection not opened')

    def send_command(self, message: bytes) -> None:
        message = bytearray(message)
        message.append(self.calculate_checksum(message))
        self._logger.info(
            'Sending bytes to SERIAL from channel {:02x} {:02x} {:02x} {:02x}'.format(
                message[0], message[1], message[2], message[3]))
        self.serial.write(message)

    @staticmethod
    def calculate_checksum(message: bytes) -> int:
        message = bytearray(message)
        checksum = (0x100 - message[0] - message[1] - message[2]) & 0x0FF
        return checksum


def create_channel(port: str, logger: Logger) -> Channel:
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_ODD
    ser.stopbits = 1
    ser.timeout = 2
    ser.open()

    return Channel(ser, logger)
