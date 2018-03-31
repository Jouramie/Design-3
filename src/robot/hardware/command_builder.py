from .command import CommandsFromStm


class CommandBuilder():

    def move(self, x_speed: int, y_speed: int, backward_forward: CommandsFromStm, left_right: CommandsFromStm) -> str:
        return 'M{}{}{}{}'.format(x_speed, y_speed, backward_forward.value, left_right.value)

    def forward(self, x_speed: int, y_speed: int, left_right: CommandsFromStm) -> str:
        return self.move(x_speed, y_speed, CommandsFromStm.FORWARD, left_right)

    def backward(self, x_speed: int, y_speed: int, left_right: CommandsFromStm) -> str:
        return self.move(x_speed, y_speed, CommandsFromStm.BACKWARD, left_right)

    def rotate(self, angle: int, positive_negative: CommandsFromStm) -> str:
        return 'R{}{}'.format(angle, positive_negative.value)
