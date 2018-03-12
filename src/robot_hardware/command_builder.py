from src.robot_hardware.command import Command


class CommandBuilder():

    def move(self, vx: str, vy: str, backward_forward: Command, left_right: Command) -> str:
        return 'M{}{}{}{}'.format(vx, vy, backward_forward.value, left_right.value)

    def forward(self, vx: int, vy: int, left_right: Command) -> str:
        return self.move(vx, vy, Command.FORWARD, left_right)

    def backward(self, vx: int, vy: int, left_right: Command) -> str:
        return self.move(vx, vy, Command.BACKWARD, left_right)

    def rotate(self, angle: int, positive_negative: Command) -> str:
        return 'R{}{}'.format(angle, positive_negative.value)
