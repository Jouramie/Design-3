from pathlib import Path

from PyQt5 import uic, QtGui
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QMainWindow

from src.station.station_controller import StationController


class StationView(QMainWindow):
    def __init__(self, model, main_controller: StationController, config: dict):
        self.__config = config
        self.model = model
        self.main_controller = main_controller
        self.ui = uic.loadUi(Path(self.__config['resources_path']['ui']))
        self.time = QTime(0, 10, 0, 0)
        self.timer = QTimer()
        self.worldCamTimer = QTimer()
        self.update_timer = QTimer()
        self.setup_button()
        super(StationView, self).__init__()

    def start_capture(self):
        self.main_controller.select_frame()
        if self.model.worldCamera_is_on:
            self.worldCamTimer.start(1)
            self.worldCamTimer.timeout.connect(self.__display_world_camera_image)

    def start_timer(self):
        self.main_controller.start_timer()
        if self.model.timer_is_on:
            self.timer.start(1000)
            self.timer.timeout.connect(self.__update_time)

    def start_robot(self):
        self.main_controller.start_robot()
        self.update_timer.start(100)
        self.update_timer.timeout.connect(self.update)

    def update(self):
        self.main_controller.update()

        # update ui with model
        # TODO __display_time()

        if self.model.countryCode is not None:
            # TODO arreter de show a chaque tick après une fois
            self.__show_selected_country()
            self.__show_cube_next_color()

    def __show_selected_country(self):
        self.main_controller.select_country()  # TODO
        self.__display_flag()
        self.__display_country_name()

    def __show_cube_next_color(self):
        self.main_controller.select_next_cube_color()  # TODO
        self.__display_next_cube_color()

    def __display_world_camera_image(self):
        ret, frame = self.model.frame.read()
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * frame.shape[2],
                             QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.ui.videoLabel.setPixmap(pixmap)

    def __update_time(self):
        # TODO Decrémenter le temps dans le controller à chaque update
        self.model.passedTime = self.model.passedTime - 1
        t = self.time.addSecs(self.model.passedTime)
        time = t.toString()
        self.ui.lcdNumber.display(time)

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
        self.ui.cube_label.setStyleSheet('background-color:' + self.model.nextCubeColor + ';')
        self.ui.cube_label.show()

    def setup_button(self):
        self.ui.StartButton.clicked.connect(self.start_capture)
        self.ui.StartButton.clicked.connect(self.start_timer)
        self.ui.StartButton.clicked.connect(self.start_robot)
