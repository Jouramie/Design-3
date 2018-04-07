from src.d3_network.command import Command
from src.robot.hardware.command.stm_command_definition.commands_to_stm import Target


class StmCommand():

    @staticmethod
    def factory(request: dict):
        if request['command'] == Command.MOVE_FORWARD:
            return StmCommand._forward(request['amplitude'])
        elif request['command'] == Command.MOVE_BACKWARD:
            return StmCommand._backward(request['amplitude'])
        elif request['command'] == Command.MOVE_ROTATE:
            return StmCommand._rotate(request['amplitude'])
        elif request['command'] == Command.MOVE_LEFT:
            return StmCommand._left(request['amplitude'])
        elif request['command'] == Command.MOVE_RIGHT:
            return StmCommand._right(request['amplitude'])
        else:
            raise NotImplementedError('Command not implemented on stm')

    @staticmethod
    def _move(target: Target, mm_distance: int) -> bytearray:
        command = bytearray()
        command.append(target.value)
        command.append(mm_distance >> 8 & 0xff)
        command.append(mm_distance & 0xff)
        return command

    @staticmethod
    def _rotate(angle: float) -> bytearray:
        if angle >= 0:
            return StmCommand._rotate_counter_clockwise(abs(int(angle)))
        elif angle < 0:
            return StmCommand._rotate_clockwise(abs(int(angle)))

    @staticmethod
    def _forward(mm_distance: float) -> bytearray:
        return StmCommand._move(Target.WHEELS_FORWARD, int(mm_distance * 10))

    @staticmethod
    def _backward(mm_distance: float) -> bytearray:
        return StmCommand._move(Target.WHEELS_BACKWARD, int(mm_distance * 10))

    @staticmethod
    def _left(mm_distance: float) -> bytearray:
        return StmCommand._move(Target.WHEELS_LEFT, int(mm_distance * 10))

    @staticmethod
    def _right(mm_distance: float) -> bytearray:
        return StmCommand._move(Target.WHEELS_RIGHT, int(mm_distance * 10))

    @staticmethod
    def _rotate_clockwise(angle: int) -> bytearray:
        return StmCommand._move(Target.WHEELS_ROTATE_CLOCKWISE, angle)

    @staticmethod
    def _rotate_counter_clockwise(angle: int) -> bytearray:
        return StmCommand._move(Target.WHEELS_ROTATE_COUNTER_CLOCKWISE, angle)


