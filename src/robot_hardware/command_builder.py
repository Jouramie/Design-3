from src.robot_hardware.command import Command


class CommandBuilder():

    def move(self, x_speed: int, y_speed: int, backward_forward: Command, left_right: Command) -> str:
        return 'M{}{}{}{}'.format(x_speed, y_speed, backward_forward.value, left_right.value)

    def forward(self, x_speed: int, y_speed: int, left_right: Command) -> str:
        return self.move(x_speed, y_speed, Command.FORWARD, left_right)

    def backward(self, x_speed: int, y_speed: int, left_right: Command) -> str:
        return self.move(x_speed, y_speed, Command.BACKWARD, left_right)

    def rotate(self, angle: int, positive_negative: Command) -> str:
        return 'R{}{}'.format(angle, positive_negative.value)
