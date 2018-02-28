from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic, QtGui
from PyQt5.QtCore import pyqtSlot, QTime, QTimer


class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        self.model = model
        self.main_controller = main_controller
        self.ui = uic.loadUi('UI/untitled.ui')
        self.time = QTime(0, 10, 0, 0)
        self.timer = QTimer()
        self.worldCamTimer = QTimer()
        self.infrared_timer = QTimer()
        self.setup_button()
        super(MainView, self).__init__()

    def start_capture(self):
        self.main_controller.select_frame()
        if self.model.worldCamera_is_on:
            self.worldCamTimer.start(1)
            self.worldCamTimer.timeout.connect(self.display_frame)

    def start_timer(self):
        self.main_controller.start_timer()
        if self.model.timer_is_on:
            self.timer.start(1000)
            self.timer.timeout.connect(self.display_time)

    def start_network(self):
        self.main_controller.start_network()
        if self.model.infrared_signal_asked:
            self.infrared_timer.start(100)
            self.infrared_timer.timeout.connect(self.check_ir_signal)

    def check_ir_signal(self):
        self.main_controller.check_ir_signal()
        if self.model.countryCode != 0:
            self.infrared_timer.stop()
            self.show_selected_country()
            self.show_cube_next_color()

    def show_selected_country(self):
        self.main_controller.select_country()
        self.display_flag()
        self.display_country_name()

    def show_cube_next_color(self):
        self.main_controller.select_next_cube_color()
        self.display_next_cube_color()

    def display_frame(self):
        ret, frame = self.model.frame.read()
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * frame.shape[2],
                             QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.ui.videoLabel.setPixmap(pixmap)

    def display_time(self):
        self.model.passedTime = self.model.passedTime - 1
        t = self.time.addSecs(self.model.passedTime)
        time = t.toString()
        self.ui.lcdNumber.display(time)

    def display_flag(self):
        flag_pixmap = QtGui.QPixmap("domain/countries/Flag_" + self.model.country.get_country_name() + ".gif")
        self.ui.flagPicture.setPixmap(flag_pixmap)
        self.ui.flagPicture.setMask(flag_pixmap.mask())
        self.ui.flagPicture.show()

    def display_country_name(self):
        self.ui.CountryName.setText(self.model.country.get_country_name())

    def display_next_cube_color(self):
        self.ui.cube_label.setStyleSheet('background-color:' + self.model.nextCubeColor + ';')
        self.ui.cube_label.show()

    def setup_button(self):
        self.ui.StartButton.clicked.connect(self.start_capture)
        self.ui.StartButton.clicked.connect(self.start_timer)
        self.ui.StartButton.clicked.connect(self.start_network)
