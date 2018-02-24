class PathCalculatorError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class PathCalculatorNoPathError(PathCalculatorError):
    def __init__(self, message):
        PathCalculatorError.__init__(self, message)

