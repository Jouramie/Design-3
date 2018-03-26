from pathlib import Path

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtWidgets import QMainWindow

from src.station.station_controller import StationController
from src.station.station_model import StationModel

import cv2


class StationView(QMainWindow):
    def __init__(self, model: StationModel, main_controller: StationController, config: dict):
        self.__config = config
        self.model = model
        self.main_controller = main_controller
        self.ui = uic.loadUi(Path(self.__config['resources_path']['ui']))
        self.time = QTime(0, 0, 0, 0)
        self.update_timer = QTimer()
        self.ui.StartButton.clicked.connect(self.start_robot)
        self.update_timer.start(100)
        self.update_timer.timeout.connect(self.update)
        super(StationView, self).__init__()

    def start_robot(self):
        self.main_controller.start_robot()

    def update(self):
        self.main_controller.update()

        # update ui with model
        self.__update_timer_display()

        if self.model.world_camera_is_on:
            self.__display_world_camera_image()

        if self.model.country_code is not None:
            self.__display_flag()
            self.__display_country_name()
            self.__display_next_cube_color()

    def __update_timer_display(self):
        t = self.time.addSecs(self.model.passed_time)
        display_time = t.toString()
        self.ui.lcdNumber.display(display_time)

    def __display_world_camera_image(self):
        _, frame = self.model.capture.read()
        resized = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        #desired_width = self.ui.videoLabel.width()
        #desired_height = self.ui.videoLabel.height()
        image = QtGui.QImage(resized, resized.shape[1], resized.shape[0], resized.shape[1] * resized.shape[2],
                             QtGui.QImage.Format_RGB888)

        #pixmap = QtGui.QPixmap(image).scaled(desired_width, desired_height, Qt.KeepAspectRatio)
        #pixmap.convertFromImage(image.rgbSwapped())
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.ui.videoLabel.setPixmap(pixmap)

    def __display_flag(self):
        image_path: Path = Path(self.__config['resources_path']['country_flag']
                                .format(country=self.model.country.get_country_name()))

        flag_pixmap = QtGui.QPixmap(str(image_path))
        self.ui.flagPicture.setPixmap(flag_pixmap)
        self.ui.flagPicture.setMask(flag_pixmap.mask())
        self.ui.flagPicture.show()

    def __display_country_name(self):
        self.ui.CountryName.setText(self.model.country.get_country_name())

    def __display_next_cube_color(self):
        self.ui.cube_label.setStyleSheet('background-color:' + self.model.next_cube_color + ';')
        self.ui.cube_label.show()
