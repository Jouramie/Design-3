from enum import Enum


class CommandsToStm(Enum):

    LEFT = 0x11
    FORWARD = 0xff
    RIGHT = 0x22
    BACKWARD = 0xbb

    WHEELS = 0x33
    ROTATE = 0x20

    GRAB_CUBE = bytearray(b'\x6c\x12\x23')
    DROP_CUBE = bytearray(b'\xdc\x12\x23')
    CAN_GRAB_CUBE = bytearray(b'\xc4\x12\x34')

    SEND_AGAIN = bytearray(b'\x46\x41\x12')


class CommandsFromStm(Enum):

    PAYS = 0xb0
    FIN_TACHE = 0xb4
    STM_COMMANDS = {PAYS, FIN_TACHE}