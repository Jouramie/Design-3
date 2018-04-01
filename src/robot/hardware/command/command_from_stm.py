from src.robot.hardware.command.not_a_country_command_exception import NotACountryCommandException
from src.robot.hardware.command.stm_command_definition.commands_from_stm import Target
from src.robot.hardware.message_corrupted_exception import MessageCorruptedException


class CommandFromStm(object):

    def __init__(self, message: bytes):
        self.target = message[0]
        self.info = message[1]
        self.checksum = message[2]
        # self._validate()

    def get_country_code(self):
        if self.target == Target.PAYS.value:
            return self.info
        else:
            raise NotACountryCommandException('Not a country code message')

    def _validate(self):
        calculated_checksum = (0x100 - self.target - self.info) & 0x0FF
        if self.checksum != calculated_checksum:
            raise MessageCorruptedException('Message could not be validated')
        if self.target not in Target.STM_COMMANDS.value:
            raise MessageCorruptedException('Target is not defined')
