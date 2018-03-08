import serial

from src.robot_software.channel.channel_listener_exception import ChannelListenerException


class ChannelListener:
    def __init__(self, serial):
        self.serial = serial

    def listen(self):
        self.listen = True
        if self.serial.is_open:
            message = str(self.serial.readline())
        else:
            raise ChannelListenerException('Serial connection not opened')

def create_channel_listener(self):
    ser = serial.Serial()
    ser.port = "/dev/ttyUSB0"
    ser.baudrate = 1200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout = 0
    ser.open()

    return ChannelListener(ser)


