from enum import Enum


class Target(Enum):
    PAYS = 0xb0
    TASK_SUCCESS = 0xfc
    TASK_FAILED = 0xec
    STM_COMMANDS = {PAYS, TASK_SUCCESS, TASK_FAILED}


class Command(Enum):
    SUCCESSFULL_TASK = bytearray(b'\xfc\x12\x34\xbe')
    UNSUCCESSFULL_TASK = bytearray(b'\xec\x12\x34\xce')
