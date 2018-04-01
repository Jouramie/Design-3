from src.robot.hardware.command.stm_command_definition.commands_to_stm import Target, Direction


class CommandBuilder():

    def move(self, target: Target, distance: int, direction: Direction) -> bytearray:
        command = bytearray()
        command.append(target.value)
        command.append(distance)
        command.append(direction.value)
        return command

    def rotate(self, direction: Direction) -> bytearray:
        return self.move(Target.ROTATE, 0, direction)

class CommandToStm(object):

    def __init__(self, target: Target, distance: int, direction: Direction):
        self.command = bytearray()
        self.command.append(target.value)
        self.command.append(distance)
        self.command.append(direction.value)

