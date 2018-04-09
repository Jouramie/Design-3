import serial

from .command.stm_command_definition import commands_to_stm, commands_from_stm
from .channel_exception import ChannelException


class Channel(object):
    def __init__(self, serial):
        self.serial = serial

    def receive_message(self) -> commands_from_stm.Feedback:
        if self.serial.is_open:

            return commands_from_stm.Feedback(self.serial.read(commands_from_stm.Message.BYTES_TO_READ.value))
        else:
            raise ChannelException('Serial connection not opened')

    def send_command(self, message: bytes) -> None:
        message = bytearray(message)
        message.append(self.calculate_checksum(message))
        self.serial.write(message)

    @staticmethod
    def calculate_checksum(message: bytes) -> int:
        message = bytearray(message)
        checksum = (0x100 - message[0] - message[1] - message[2]) & 0x0FF
        print('{:02x}'.format(checksum))
        return checksum


def create_channel(port: str) -> Channel:
    ser = serial.Serial()
    ser.port = port
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = 1
    ser.timeout = 2
    ser.open()

    return Channel(ser)
