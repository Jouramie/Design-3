from src.robot.hardware.command.stm_command_definition.commands_to_stm import Target, Direction


class StmCommandBuilder():

    def _move(self, target: Target, distance: int, direction: Direction) -> bytearray:
        command = bytearray()
        command.append(target.value)
        command.append(distance)
        command.append(direction.value)
        return command

    def rotate(self, direction: Direction) -> bytearray:
        return self._move(Target.ROTATE, 0, direction)

    def forward(self, distance: int) -> bytearray:
        return self._move(Target.WHEELS, distance, Direction.FORWARD)

    def backward(self, distance: int) -> bytearray:
        return self._move(Target.WHEELS, distance, Direction.BACKWARD)

    def left(self, distance: int) -> bytearray:
        return self._move(Target.WHEELS, distance, Direction.LEFT)

    def right(self, distance: int) -> bytearray:
        return self._move(Target.WHEELS, distance, Direction.RIGHT)
