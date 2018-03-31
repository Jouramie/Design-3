from .command import CommandsToStm


class CommandBuilder():

    def move(self, x_speed: int, y_speed: int, backward_forward: CommandsToStm, left_right: CommandsToStm) -> str:
        return 'M{}{}{}{}'.format(x_speed, y_speed, backward_forward.value, left_right.value)

    def forward(self, x_speed: int, y_speed: int, left_right: CommandsToStm) -> str:
        return self.move(x_speed, y_speed, CommandsToStm.FORWARD, left_right)

    def backward(self, x_speed: int, y_speed: int, left_right: CommandsToStm) -> str:
        return self.move(x_speed, y_speed, CommandsToStm.BACKWARD, left_right)

    def rotate(self, angle: int, positive_negative: CommandsToStm) -> str:
        return 'R{}{}'.format(angle, positive_negative.value)
