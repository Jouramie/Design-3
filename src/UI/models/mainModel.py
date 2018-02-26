class MainModel(object):
    def __init__(self):
        self.passedTime = 0
        self.country = "Country not yet selected"
        self.nextCubeColor = ""
        self.frame = ""
        self.countryCode = 0
        self.timer_is_on = False
        self.worldCamera_is_on = False

        self._update_functions = []
        self.running = False

    def subscribe_update_function(self, function):
        if function not in self._update_functions:
            self._update_functions.append(function)

    def unsubscribe_update_function(self, function):
        if function in self._update_functions:
            self._update_functions.remove(function)

    def annonce_update(self):
        for function in self._update_functions:
            function()