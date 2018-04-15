import subprocess
from pathlib import Path

import cv2
from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QMainWindow

from src.station.station_controller import StationController
from src.station.station_model import StationModel
from src.vision.frame_drawer import FrameDrawer
from src.domain.objects.color import Color


class StationView(QMainWindow):
    def __init__(self, model: StationModel, station_controller: StationController, frame_drawer: FrameDrawer,
                 config: dict):
        self.__config = config

        self.model = model
        self.station_controller = station_controller
        self.frame_drawer = frame_drawer

        self.ui = uic.loadUi(Path(self.__config['resources_path']['ui']))
        self.time = QTime(0, 0, 0, 0)
        self.update_timer = QTimer()
        self.update_timer.start(100)
        self.update_timer.timeout.connect(self.update)

        self.ui.StartButton.clicked.connect(self.start_robot)
        self.ui.StopButton.clicked.connect(self.stop_robot)

        super(StationView, self).__init__()

    def start_robot(self):
        self.station_controller.start_robot()

    def stop_robot(self):
        subprocess.run(['ssh', 'design3@10.42.0.1', 'pkill', 'python3'])

    def update(self):
        self.station_controller.update()

        self.__draw_environment(self.model.frame)

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
        resized_image = cv2.resize(self.model.frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        image = QtGui.QImage(resized_image, resized_image.shape[1], resized_image.shape[0],
                             resized_image.shape[1] * resized_image.shape[2],
                             QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.ui.videoLabel.setPixmap(pixmap)

    def __display_flag(self):
        image_path: Path = Path(self.__config['resources_path']['country_flag']
                                .format(country=self.model.country.name))

        flag_pixmap = QtGui.QPixmap(str(image_path))
        self.ui.flagPicture.setPixmap(flag_pixmap)
        self.ui.flagPicture.setMask(flag_pixmap.mask())
        self.ui.flagPicture.show()

    def __display_country_name(self):
        self.ui.CountryName.setText(self.model.country.name)

    def __display_next_cube_color(self):
        if self.model.next_cube is None:
            self.ui.cube_label.setStyleSheet('background-color:' + Color.TRANSPARENT.name.lower() + ';')
        else:
            self.ui.cube_label.setStyleSheet('background-color:' + self.model.next_cube.color.name.lower() + ';')
        self.ui.cube_label.show()

    def __draw_environment(self, frame):
        if self.__config['user_interface']['draw_vision_cubes']:
            if self.model.vision_environment is not None:
                self.frame_drawer.draw_vision_environment(frame, self.model.vision_environment)

        if self.model.real_world_environment is not None:
            self.frame_drawer.draw_real_world_environment(frame, self.model.real_world_environment)

        if self.model.planned_path is not None and self.model.planned_path:
            self.frame_drawer.draw_planned_path(frame, self.model.planned_path)

        if self.model.real_path is not None and self.model.real_path:
            self.frame_drawer.draw_real_path(frame, self.model.real_path)

        if self.model.robot is not None:
            self.frame_drawer.draw_robot(frame, self.model.robot)
