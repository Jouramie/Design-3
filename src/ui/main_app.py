import sys
from PyQt5.QtWidgets import QApplication
from station_controller.station_controller import StationController
from station_controller.station_model import StationModel
from src.ui.views.main_view import StationView


class App(QApplication):
    def __init__(self, network, logger, config: dict):
        super(App, self).__init__([''])
        self.main_model = StationModel()
        self.main_controller = StationController(self.main_model, network, logger, config)
        self.main_view = StationView(self.main_model, self.main_controller)
        self.main_view.ui.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())
