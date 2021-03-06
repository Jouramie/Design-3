class Command(object):
    RESET = 'reset'
    START = 'start'
    HELLO = 'hello'
    INFRARED_SIGNAL = 'infrared-signal'
    END_SIGNAL = 'end-signal'
    CAN_I_GRAB = 'can-i-grab'
    GRAB = 'grab-it'
    DROP = 'drop-it'
    MOVE_FORWARD = 'move-forward'
    MOVE_BACKWARD = 'move-backward'
    MOVE_ROTATE = 'move-rotate'
    MOVE_RIGHT = 'move-right'
    MOVE_LEFT = 'move-left'

    GRAB_CUBE_FAILURE = 'grab-cube-failure'
    EXECUTED_ALL_REQUESTS = 'requests-were-executed-commander'

    ACTION = 'action'
