from src.d3_network.command import Command


class Action(object):
    def __init__(self, command: Command):
        self.command = command

    def __str__(self):
        return "{}".format(self.command)

    def to_command(self):
        return {'command': self.command}


class Grab(Action):
    def __init__(self):
        super().__init__(Command.GRAB)


class Drop(Action):
    def __init__(self):
        super().__init__(Command.DROP)


class IR(Action):
    def __init__(self):
        super().__init__(Command.INFRARED_SIGNAL)


class CanIGrab(Action):
    def __init__(self):
        super().__init__(Command.CAN_I_GRAB)


class LightItUp(Action):
    def __init__(self):
        super().__init__(Command.END_SIGNAL)


class Hello(Action):
    def __init__(self):
        super().__init__(Command.HELLO)


class Reset(Action):
    def __init__(self):
        super().__init__(Command.RESET)


class Start(Action):
    def __init__(self):
        super().__init__(Command.START)


class Movement(Action):
    def __init__(self, command: Command, amplitude):
        super().__init__(command)
        self.amplitude = amplitude

    def __eq__(self, other):
        return self.amplitude == other.amplitude

    def __str__(self):
        return "{} : {}".format(self.command, self.amplitude)

    def to_command(self):
        return {'command': self.command, 'amplitude': self.amplitude}


class Rotate(Movement):
    def __init__(self, amplitude):
        if abs(amplitude) > 100:
            super().__init__(Command.MOVE_ROTATE, amplitude * 0.95)
        else:
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
