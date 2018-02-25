import cv2
from PyQt5 import QtWidgets, QtCore, uic, QtGui

class MainModel(object):
    def __init__(self):
        self.time = QtCore.QTime(0, 10, 0, 0)
        self.passedTime = 0
        self.timer = QtCore.QTimer()
        self.countryName = "Country not yet selected"
        self.nextCubeColor = ""
        self.worldCamTimer = QtCore.QTimer()
        self.frame = ""
        self.countryCode = 0

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