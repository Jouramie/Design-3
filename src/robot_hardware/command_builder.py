from src.robot_hardware.command import Command


class CommandBuilder():

    def move(self, vx: str, vy: str, backward_forward: str, left_right: str) -> str:
        return 'M{}{}{}{}'.format(vx, vy, backward_forward, left_right)

    def forward(self, vx: int, vy: int, left_right: str) -> str:
        return self.move(vx, vy, Command.forward, left_right)

    def backward(self, vx: int, vy: int, left_right: str) -> str:
        return self.move(vx, vy, Command.backward, left_right)

    def right(self, vx: int, vy: int, backward_forward: str) -> str:
        return self.move(vx, vy, backward_forward, Command.right)

    def left(self, vx: int, vy: int, backward_forward:str) -> str:
        return self.move(vx, vy, backward_forward, Command.left)

    def rotate(self, alpha: int, positive_negative: str) -> str:
        return 'R{}{}'.format(alpha, positive_negative)

