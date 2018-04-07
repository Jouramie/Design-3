from src.d3_network.command import Command


class Movement(object):
    def __init__(self, command: Command, amplitude):
        self.amplitude = amplitude
        self.command = command

    def __eq__(self, other):
        return self.amplitude == other.amplitude

    def __str__(self):
        return "{} : {}".format(self.command, self.amplitude)


class Rotate(Movement):
    def __init__(self, amplitude):
        super().__init__(Command.MOVE_ROTATE, amplitude)


class Forward(Movement):
    def __init__(self, amplitude):
        super().__init__(Command.MOVE_FORWARD, amplitude)


class Backward(Movement):
    def __init__(self, amplitude):
        super().__init__(Command.MOVE_BACKWARD, amplitude)


class Left(Movement):
    def __init__(self, amplitude):
        super().__init__(Command.MOVE_LEFT, amplitude)


class Right(Movement):
    def __init__(self, amplitude):
        super().__init__(Command.MOVE_RIGHT, amplitude)
