import serial

from .command.stm_command import CommandsToStm
from .channel_exception import ChannelException


class Channel(object):

    def __init__(self, serial):
        self.serial = serial

    def receive_message(self):
        if self.serial.is_open:
            return str(self.serial.readline())
        else:
            raise ChannelException('Serial connection not opened')

    def send_command(self, message: bytes):
        message = bytearray(message)
        message.append(self.calculate_checksum(message))
        self.serial.write(message)

    def ask_repeat(self):
        self.send_command(CommandsToStm.SEND_AGAIN.value)

    @staticmethod
    def calculate_checksum(message: bytes) -> int:
        message = bytearray(message)
        checksum = (0x100 - message[0] - message[1] - message[2]) & 0x0FF
        return checksum

def create_channel(port: str):
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = 1
    ser.timeout = 2
    ser.open()

    return Channel(ser)
