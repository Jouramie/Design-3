import cv2

from src.domain.countryLoader import CountryLoader


class MainController(object):
    def __init__(self, model):
        self.model = model
        self.countryLoader = CountryLoader()
        self.set_country_code(48)

    def set_country_code(self, country_code):
        self.model.countryCode = country_code

    def start_timer(self):
        self.model.timer.start(1000)
        print("start timer")

    def select_flag(self):
        try:
            countries = self.countryLoader.get_country_list()
            selected_country = countries[self.model.countryCode]
            self.set_country_name(selected_country[0])

        except FileNotFoundError:
            print("This country doesn't exists")

    def set_country_name(self, country_name):
        self.model.countryName = country_name

    def select_next_cube_color(self):
        self.model.nextCubeColor = "black"

    def select_frame(self):
        self.model.frame = cv2.VideoCapture(0)
        self.model.worldCamTimer.start(1)
