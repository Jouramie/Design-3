class CameraError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class CameraInitializationError(CameraError):
    def __init__(self, message):
        CameraError.__init__(self, message)
