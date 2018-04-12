from enum import Enum


class Target(Enum):
    PAYS = 0xb0
    TASK_SUCCESS = 0xfc
    TASK_FAILED = 0xec
    STM_COMMANDS = {PAYS, TASK_SUCCESS, TASK_FAILED}


class Message(Enum):
    SUCCESSFULL_TASK = bytearray(b'\xfc\x12\x34\xbe')
    UNSUCCESSFULL_TASK = bytearray(b'\xec\x12\x34\xce')
    TASK_CUBE_FAILED = bytearray(b'\xec\x6c\x6c\x3c')
    TASK_RECEIVED_ACK = bytearray(b'\xcd\x2a\x3a\xcf')
    NOTHING = bytearray(b'')
    OPEN_CLOSE_MSG = bytearray(b'\xff')
    MESSAGES_TO_IGNORE = [OPEN_CLOSE_MSG, NOTHING]
    BYTES_TO_READ = 4


class Feedback(object):
    TASK_SUCCESS = 'task-success'
    TASK_FAILED = 'task-failure'
    TASK_CUBE_FAILED = 'task-cube-failure'
    TASK_RECEIVED = 'task-received'
    COUNTRY = 'country'
    HEY = 'hey'

    def __init__(self, message: bytearray):
        self.country = None
        self.message = None
        if message in Message.MESSAGES_TO_IGNORE.value:
            self.type = Feedback.HEY
        elif message == Message.SUCCESSFULL_TASK.value:
            self.type = Feedback.TASK_SUCCESS
        elif message == Message.UNSUCCESSFULL_TASK.value:
            self.type = Feedback.TASK_FAILED
        elif message == Message.TASK_RECEIVED_ACK.value:
            self.type = Feedback.TASK_RECEIVED
        elif message == Message.TASK_CUBE_FAILED.value:
            self.type = Feedback.TASK_CUBE_FAILED
        elif message[0] == Target.PAYS.value:
            self.type = Feedback.COUNTRY
            self.country = message[1]
        else:
            self.type = Feedback.HEY
            self.message = message
