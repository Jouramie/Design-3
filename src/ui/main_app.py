from PyQt5.QtWidgets import QApplication

from src.ui.views.main_view import StationView
from station.station_controller import StationController
from station.station_model import StationModel


class App(QApplication):
    def __init__(self, network, logger, config: dict):
        super(App, self).__init__([''])
        self.main_model = StationModel()
        self.main_controller = StationController(self.main_model, network, logger, config)
        self.main_view = StationView(self.main_model, self.main_controller, config)
        self.main_view.ui.show()

