from src.robot.hardware.command.stm_command_definition.commands_to_stm import Target, Direction, Angle


class StmCommandBuilder():

    def _move(self, target: Target, mm_distance: int) -> bytearray:
        command = bytearray()
        command.append(target.value)
        command.append(mm_distance >> 8 & 0xff)
        command.append(mm_distance & 0xff)
        return command

    def rotate_clockwise(self, angle: Angle) -> bytearray:
        return self._move(Target.WHEELS_ROTATE_CLOCKWISE, angle.value)

    def rotate_counter_clockwise(self, angle: Angle):
        return self._move(Target.WHEELS_ROTATE_COUNTER_CLOCKWISE, angle.value)

    def forward(self, mm_distance: int) -> bytearray:
        return self._move(Target.WHEELS_FORWARD, mm_distance)

    def backward(self, mm_distance: int) -> bytearray:
        return self._move(Target.WHEELS_BACKWARD, mm_distance)

    def left(self, mm_distance: int) -> bytearray:
        return self._move(Target.WHEELS_LEFT, mm_distance)

    def right(self, mm_distance: int) -> bytearray:
        return self._move(Target.WHEELS_RIGHT, mm_distance)
