import serial

from src.robot.hardware.channel_listen_exception import ChannelException


class Channel:

    def __init__(self, serial):
        self.serial = serial

    def listen(self):
        if self.serial.is_open:
            return str(self.serial.readline())
        else:
            raise ChannelException('Serial connection not opened')

    def write(self, message: bytes):
        message = bytearray(message)
        total = 0
        for h in message:
            total += h
        checksum = 0x100-total
        message.append(checksum)
        self.serial.write(message)

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
