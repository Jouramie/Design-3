from src.domain.vision_environment.robot import Robot
from src.domain.vision_environment.vision_environment import VisionEnvironment
from src.domain.color import Color
from src.domain.country import Country


class StationModel(object):
    def __init__(self):
        self.start_time = 0
        self.passed_time = 0

        self.country: Country = "Country not yet selected"
        self.country_code: int = None
        self.next_cube_color: Color = None

        self.frame = None

        self.robot: Robot = None
        self.vision_environment: VisionEnvironment = None

        self.robot_is_started = False
        self.robot_is_moving = False
        self.timer_is_on = False
        self.world_camera_is_on = False
        self.infrared_signal_asked = False

        self.planned_path = None
        self.real_path = []

        self._update_functions = []
        self.running = False

    def subscribe_update_function(self, func):
        if func not in self._update_functions:
            self._update_functions.append(func)

    def unsubscribe_update_function(self, func):
        if func in self._update_functions:
            self._update_functions.remove(func)

    def announce_update(self):
        for func in self._update_functions:
            func()
