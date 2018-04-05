class Movement(object):
    def __init__(self, amplitude):
        self.amplitude = amplitude

    def __eq__(self, other):
        return self.amplitude == other.amplitude

    def __str__(self):
        return "movement: {}".format(self.amplitude)


class Rotate(Movement):
    def __init__(self, amplitude):
        super().__init__(amplitude)

    def __str__(self):
        return "move-rotate: {}".format(self.amplitude)


class Forward(Movement):
    def __init__(self, amplitude):
        super().__init__(amplitude)

    def __str__(self):
        return "move-forward: {}".format(self.amplitude)


class Backward(Movement):
    def __init__(self, amplitude):
        super().__init__(amplitude)

    def __str__(self):
        return "move-backward: {}".format(self.amplitude)

class Left(Movement):
    def __init__(self, amplitude):
        super().__init__(amplitude)

    def __str__(self):
        return "move-right: {}".format(self.amplitude)

class Right(Movement):
    def __init__(self, amplitude):
        super().__init__(amplitude)

    def __str__(self):
        return "move-left: {}".format(self.amplitude)

