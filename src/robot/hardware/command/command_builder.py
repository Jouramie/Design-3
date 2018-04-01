from src.robot.hardware.command.stm_command import CommandsToStm


class CommandBuilder():

    def move(self, target: CommandsToStm, distance: int, direction: CommandsToStm) -> bytearray:
        command = bytearray()
        command.append(target.value)
        command.append(distance)
        command.append(direction.value)
        return command

    def rotate(self, direction: CommandsToStm) -> bytearray:
        return self.move(CommandsToStm.ROTATE, 0, CommandsToStm.LEFT)
