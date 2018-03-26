import serial

from .channel_listen_exception import ChannelException


class Channel:

    def __init__(self, serial):
        self.serial = serial

    def listen(self):
        if self.serial.is_open:
            return str(self.serial.readline())
        else:
            raise ChannelException('Serial connection not opened')

    def write(self, message: bytes):
        self.serial.write(message)

def create_channel():
    ser = serial.Serial()
    ser.port = "/dev/ttyUSB0"
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = 1
    ser.timeout = 2
    ser.open()

    return Channel(ser)
