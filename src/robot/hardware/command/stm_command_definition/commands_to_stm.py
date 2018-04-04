from enum import Enum


class Target(Enum):

    WHEELS = 0x33
    ROTATE = 0x20

    WHEELS_LEFT = 0x31
    WHEELS_FORWARD = 0x3f
    WHEELS_RIGHT = 0x32
    WHEELS_BACKWARD = 0x3b

    WHEELS_ROTATE_CLOCKWISE = 0x20
    WHEELS_ROTATE_COUNTER_CLOCKWISE = 0x21


class Direction(Enum):

    LEFT = 0x11
    FORWARD = 0xff
    RIGHT = 0x22
    BACKWARD = 0xbb


class Command(Enum):

    GRAB_CUBE = bytearray(b'\x6c\x12\x23')
    DROP_CUBE = bytearray(b'\xdc\x12\x23')
    CAN_GRAB_CUBE = bytearray(b'\xc4\x12\x34')
    LIGHT_IT_UP = bytearray(b'\xee\x12\x34')
    SEEK_FLAG = bytearray(b'\x12\x34\x56')

    SEND_AGAIN = bytearray(b'\x46\x41\x12')


class Angle(Enum):
    NORTH = 0x5a        # 90
    NORTH_WEST = 0x87   # 135
    WEST = 0xb4         # 180
    SOUTH_WEST = 0xe1   # 225
    SOUTH = 0x10e       # 270
    SOUTH_EAST = 0x13b  # 315
    EAST = 0x0          # 0
    NORTH_EAST = 0x2d   # 45
