from src.domain.environments.real_world_environment import RealWorldEnvironment
from src.domain.environments.vision_environment import VisionEnvironment
from src.domain.objects.country import Country
from src.domain.objects.flag_cube import FlagCube
from src.domain.objects.robot import Robot
from .state import State


class StationModel(object):
    def __init__(self):
        self.start_time = 0
        self.passed_time = 0

        self.country: Country = None
        self.country_code: int = None
        self.current_cube_index = 0
        self.next_cube: FlagCube = None
        self.target_cube = None
        self.last_grabbed_cube = None

        self.frame = None

        self.robot: Robot = None
        self.vision_environment: VisionEnvironment = None
        self.real_world_environment: RealWorldEnvironment = None

        self.current_state = State.NOT_STARTED
        self.next_state = None
        self.world_camera_is_on = False

        self.original_planned_path = None
        self.revised_planned_path = None
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
