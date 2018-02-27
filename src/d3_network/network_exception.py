class NetworkException(Exception):
    def __init__(self, message: str = 'Something went wrong...'):
        super().__init__(message)
