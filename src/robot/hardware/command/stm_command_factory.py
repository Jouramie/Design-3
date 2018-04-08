from src.d3_network.command import Command
from src.robot.hardware.command.stm_command_definition import commands_to_stm
from src.robot.hardware.command.stm_command_definition.commands_to_stm import Target


class StmCommand():

    @staticmethod
    def factory(request: dict) -> bytearray:
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
        elif request['command'] == Command.INFRARED_SIGNAL:
            return StmCommand._ir_signal()
        elif request['command'] == Command.GRAB:
            return StmCommand._grab_cube()
        elif request['command'] == Command.CAN_I_GRAB:
            return StmCommand._can_grab_cube()
        elif request['command'] == Command.DROP:
            return StmCommand._drop_cube()
        elif request['command'] == Command.END_SIGNAL:
            return StmCommand._light_led()
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

    @staticmethod
    def _ir_signal() -> bytearray:
        return commands_to_stm.Command.IR_SIGNAL.value

    @staticmethod
    def _grab_cube() -> bytearray:
        return commands_to_stm.Command.GRAB_CUBE.value

    @staticmethod
    def _can_grab_cube() -> bytearray:
        return commands_to_stm.Command.CAN_GRAB_CUBE.value

    @staticmethod
    def _drop_cube() -> bytearray:
        return commands_to_stm.Command.DROP_CUBE.value

    @staticmethod
    def _light_led() -> bytearray:
        return commands_to_stm.Command.LIGHT_IT_UP.value

