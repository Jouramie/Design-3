from enum import Enum


class State(Enum):
    NOT_STARTED = 0
    GETTING_COUNTRY_CODE = 1
    TRAVELING_TO_CUBE_REPOSITORY = 2
    ADJUSTING_IN_FRONT_CUBE_REPOSITORY = 3
    MOVING_TO_GRAB_CUBE = 4
    GRABBING_CUBE = 5
    MOVING_OUT_OF_DANGER_ZONE = 6
    TRAVELLING_TO_DROP_CUBE = 7
    EXITING_TARGET_ZONE_AND_LIGHT = 8
    RESETTING = -1
    WORKING = -2