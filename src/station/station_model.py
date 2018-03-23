class StationModel(object):
    def __init__(self):
        self.start_time = 0
        self.passed_time = 0
        self.country = "Country not yet selected"
        self.next_cube_color = None
        self.frame = None
        self.country_code = None
        self.robot_is_started = False
        self.robot_is_moving = False
        self.timer_is_on = False
        self.world_camera_is_on = False
        self.infrared_signal_asked = False
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