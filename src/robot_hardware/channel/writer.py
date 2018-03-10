import serial

from src.robot_hardware.channel.listener import create_channel_listener
from src.robot_hardware.command import Command
from src.robot_hardware.command_builder import CommandBuilder


class ChannelWriter():

    def __init__(self, serial):
        self.serial = serial

    def write(self, message: str):
        self.serial.write(wrapper(message))

def wrapper(message):
    return '{}\n'.format(message).encode()

def create_channel_writer():
    ser = serial.Serial()
    ser.port = "/dev/ttyUSB0"
    ser.baudrate = 115200
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.open()
    return ChannelWriter(ser)
