from enum import Enum
from .message_corrupted_exception import MessageCorruptedException


class CommandsFromStm(Enum):

    PAYS = 0xb0
    PREHENSEUR_UP = 0xb1
    PREHENSEUR_STOP = 0xb2
    PREHENSEUR_DOWN = 0xb3
    FIN_TACHE = 0xb4
    STM_COMMANDS = {PAYS, PREHENSEUR_UP, PREHENSEUR_STOP, PREHENSEUR_DOWN, FIN_TACHE}


class CommandsToStm(Enum):

    BACKWARD = 'B'
    FORWARD = 'F'
    RIGHT = 'R'
    LEFT = 'L'
    POSITIVE = 'P'
    NEGATIVE = 'N'

    GRAB_CUBE = bytearray(b'\x6c\x12\x23')
    DROP_CUBE = bytearray(b'\xdc\x12\x23')
    CAN_GRAB_CUBE = bytearray(b'\xc4\x12\x34')

    SEND_AGAIN = bytearray(b'\x46\x41\x12')


class CommandFromStm:

    def __init__(self, message: bytes):
        self.target = message[0]
        self.info = message[1]
        self.checksum = message[2]
        # self._validate()

    def get_country_code(self):
        if self.target is CommandsFromStm.PAYS.value:
            return self.info
        else:
            return 'Not a country code message'

    def _validate(self):
        calculated_checksum = (0x100 - self.target - self.info) & 0x0FF
        if self.checksum != calculated_checksum:
            raise MessageCorruptedException('Message could not be validated')
        if self.target not in CommandsFromStm.STM_COMMANDS.value:
            raise MessageCorruptedException('Target is not defined')
