import serial

from .channel_listener_exception import ChannelListenerException


class ChannelListener:

    def __init__(self, serial):
        self.serial = serial

    def listen(self):
        if self.serial.is_open:
            return str(self.serial.readline())
        else:
            raise ChannelListenerException('Serial connection not opened')

def create_channel_listener():
    ser = serial.Serial()
    ser.port = "/dev/ttyUSB0"
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = 1
    ser.timeout = 2
    ser.open()

    return ChannelListener(ser)
