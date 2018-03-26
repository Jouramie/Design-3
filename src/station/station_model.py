class StationModel(object):
    def __init__(self):
        self.start_time = 0
        self.passed_time = 0
        self.country = "Country not yet selected"
        self.table = None
        self.robot = None
        self.next_cube_color = None
        self.capture = None
        self.country_code = None
        self.robot_is_started = False
        self.robot_is_moving = False
        self.timer_is_on = False
        self.world_camera_is_on = False
        self.infrared_signal_asked = False
        self.projected_path = [(55, 100), (210, 40), (160, 150), (230, 180)]
        self.real_path = [(50, 100), (200, 30), (150, 150), (200, 200)]
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
