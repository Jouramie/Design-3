from enum import Enum


class Target(Enum):

    PAYS = 0xb0
    STM_COMMANDS = {PAYS}

class Command(Enum):

    END_OF_TASK = bytearray(b'\xfc\x12\x34')
