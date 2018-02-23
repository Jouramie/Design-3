from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.QtCore import pyqtSlot, QTimer


class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        self.model = model
        self.main_controller = main_controller
        self.ui = uic.loadUi('untitled.ui')
        self.setup_button()
        super(MainView, self).__init__()

    @pyqtSlot()
    def start_capture(self):
        self.main_controller.select_frame()
        self.model.worldCamTimer.timeout.connect(self.showFrame)

    @pyqtSlot()
    def start_timer(self):
        self.main_controller.start_timer()
        self.model.timer.timeout.connect(self.showTime)

    @pyqtSlot()
    def show_flag(self):
        self.main_controller.select_flag()
        self.display_flag()

    @pyqtSlot()
    def show_country_name(self):
        self.main_controller.select_country_name()
        self.display_country_name()

    @pyqtSlot()
    def show_cube_next_color(self):
        self.main_controller.select_next_cube_color()
        self.display_next_cube_color()

    def showFrame(self):
        ret, frame = self.model.frame.read()
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * frame.shape[2], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.ui.videoLabel.setPixmap(pixmap)

    def showTime(self):
        self.model.passedTime = self.model.passedTime - 1
        t = self.model.time.addSecs(self.model.passedTime)
        time = t.toString()
        self.ui.lcdNumber.display(time)

    def display_flag(self):
        flag_pixmap = QtGui.QPixmap("../domain/country/Flag_" + self.model.flag + ".gif")
        self.ui.flagPicture.setPixmap(flag_pixmap)
        self.ui.flagPicture.setMask(flag_pixmap.mask())
        self.ui.flagPicture.show()

    def display_country_name(self):
        self.ui.CountryName.setText(self.model.countryName)

    def display_next_cube_color(self):
        self.ui.cube_label.setStyleSheet('background-color:' + self.model.nextCubeColor +';')
        self.ui.cube_label.show()

    def setup_button(self):
        self.ui.StartButton.clicked.connect(self.start_capture)
        self.ui.StartButton.clicked.connect(self.start_timer)
        self.ui.StartButton.clicked.connect(self.show_flag)
        self.ui.StartButton.clicked.connect(self.show_cube_next_color)
        self.ui.StartButton.clicked.connect(self.show_country_name)
