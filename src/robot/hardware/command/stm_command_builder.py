from src.robot.hardware.command.stm_command_definition.commands_to_stm import Target


class StmCommandBuilder():

    def _move(self, target: Target, mm_distance: int) -> bytearray:
        command = bytearray()
        command.append(target.value)
        command.append(mm_distance >> 8 & 0xff)
        command.append(mm_distance & 0xff)
        return command

    def rotate(self, angle: float) -> bytearray:
        if angle >= 0:
            return self._rotate_counter_clockwise(abs(int(angle)))
        elif angle < 0:
            return self._rotate_clockwise(abs(int(angle)))

    def forward(self, mm_distance: float) -> bytearray:
        return self._move(Target.WHEELS_FORWARD, int(mm_distance * 10))

    def backward(self, mm_distance: float) -> bytearray:
        return self._move(Target.WHEELS_BACKWARD, int(mm_distance * 10))

    def left(self, mm_distance: float) -> bytearray:
        return self._move(Target.WHEELS_LEFT, int(mm_distance * 10))

    def right(self, mm_distance: float) -> bytearray:
        return self._move(Target.WHEELS_RIGHT, int(mm_distance * 10))

    def _rotate_clockwise(self, angle: int) -> bytearray:
        return self._move(Target.WHEELS_ROTATE_CLOCKWISE, angle)

    def _rotate_counter_clockwise(self, angle: int) -> bytearray:
        return self._move(Target.WHEELS_ROTATE_COUNTER_CLOCKWISE, angle)
