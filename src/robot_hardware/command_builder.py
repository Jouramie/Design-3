from src.robot_hardware.command import Command


class CommandBuilder():

    def __move(self, vx: str, vy: str, backward_forward: Command, left_right: Command) -> str:
        return 'M{}{}{}{}'.format(vx, vy, backward_forward, left_right)

    def forward(self, vx: int, vy: int, left_right: Command) -> str:
        return self.__move(vx, vy, Command.forward.value, left_right.value)

    def backward(self, vx: int, vy: int, left_right: Command) -> str:
        return self.__move(vx, vy, Command.backward.value, left_right.value)

    def rotate(self, angle: int, positive_negative: Command) -> str:
        return 'R{}{}'.format(angle, positive_negative.value)
