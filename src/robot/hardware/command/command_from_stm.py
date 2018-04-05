from src.robot.hardware.command.not_a_country_command_exception import NotACountryCommandException
from src.robot.hardware.command.stm_command_definition.commands_from_stm import Target
from src.robot.hardware.message_corrupted_exception import MessageCorruptedException


class CommandFromStm(object):

    def __init__(self, message: str):
        self.raw_command = "".join("{:02x}".format(ord(c)) for c in message)
        self.command = self.raw_command[4:10] + self.raw_command[10:12]
        self.target = int(self.command[0:2], 16)
        self.info = int(self.command[2:4], 16)
        self.info2 = int(self.command[4:6], 16)
        self.checksum = int(self.command[6:8], 16)
        # self._validate()

    def get_country_code(self):
        if self.target == Target.PAYS.value:
            return self.info
        else:
            raise NotACountryCommandException('Not a country code message')

    def _validate(self):
        calculated_checksum = (0x100 - self.target - self.info - self.info2) & 0x0FF
        if self.checksum != calculated_checksum:
            raise MessageCorruptedException(
                'Message could not be validated. Calculated checksum : {}, current checksum : {}'.format(
                    hex(calculated_checksum), hex(self.checksum)))
        if self.target not in Target.STM_COMMANDS.value:
            raise MessageCorruptedException('Target is not defined')
        else:
            return True
