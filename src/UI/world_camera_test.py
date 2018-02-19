import cv2
from PyQt5 import QtWidgets, QtCore, uic, QtGui

class Capture():
    def __init__(self, MainWindow):
        self.mainWindow = MainWindow
        self.c = cv2.VideoCapture(0)

    def startCapture(self):
        print("pressed start")
        self.timer = QtCore.QTimer(self.mainWindow)
        self.timer.timeout.connect(self.showFrame)
        self.timer.start(1);

    def endCapture(self):
        print("pressed End")
        self.timer.stop()

    def showFrame(self):
        ret, frame = self.c.read()
        image = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * frame.shape[2], QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap()
        pixmap.convertFromImage(image.rgbSwapped())
        self.mainWindow.videoLabel.setPixmap(pixmap)

class Timer():
    def __init__(self, MainWindow):
        self.QLCDNumber = MainWindow.lcdNumber
        self.time = QtCore.QTime(0, 10, 0, 0)
        self.passedTime = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showTime)

    def startTimer(self):
        self.timer.start(1000)
        print("start timer")

    def stopTimer(self):
        self.timer.stop()
        print("stop timer")

    def showTime(self):
        self.passedTime = self.passedTime - 1
        t = self.time.addSecs(self.passedTime)
        time = t.toString()
        self.QLCDNumber.display(time)

class Flag():
    def __init__(self, MainWindow):
        self.flag_label = MainWindow.flag_label

class Window(QtWidgets.QWidget):
    def __init__(self):
        self.MainWindow = uic.loadUi('untitled.ui')

        self.capture = Capture(self.MainWindow)
        self.timer = Timer(self.MainWindow)

        self.MainWindow.StartButton.clicked.connect(self.capture.startCapture)
        self.MainWindow.StartButton.clicked.connect(self.timer.startTimer)

        self.MainWindow.StopButton.clicked.connect(self.capture.endCapture)
        self.MainWindow.StopButton.clicked.connect(self.timer.stopTimer)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.MainWindow.show()
    sys.exit(app.exec_())