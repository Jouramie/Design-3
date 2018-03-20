class StationModel(object):
    def __init__(self):
        self.passedTime = 0
        self.country = "Country not yet selected"
        self.nextCubeColor = ""
        self.frame = ""
        self.countryCode = None
        self.network_is_on = False
        self.robot_is_moving = False
        self.timer_is_on = False
        self.worldCamera_is_on = False
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
