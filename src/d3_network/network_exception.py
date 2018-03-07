from .command import Command


class NetworkException(Exception):
    def __init__(self, message: str = 'Something went wrong...'):
        super().__init__(message)


class WrongCommand(NetworkException):
    def __init__(self, expected: Command, received: Command):
        super().__init__("Wrong command received. Expected: {expected}. Received: {received}."
                         .format(expected=expected, received=received))


class MessageNotReceivedYet(NetworkException):
    def __init__(self):
        super().__init__("No message has been received yet or message is incomplete.")
