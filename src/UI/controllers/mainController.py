import cv2

from src.domain.countryLoader import CountryLoader


class MainController(object):
    def __init__(self, model):
        self.model = model
        self.countryLoader = CountryLoader()
        self.set_country_code(34) #Enter country code here

    def set_country_code(self, country_code):
        self.model.countryCode = country_code

    def start_timer(self):
        self.model.timer_is_on = True
        print("start timer")

    def select_country(self):
        try:
            countries = self.countryLoader.get_country_list()
            selected_country = countries[self.model.countryCode]
            self.model.country = selected_country

        except FileNotFoundError:
            print("This countries doesn't exists")

    def select_next_cube_color(self):
        stylized_flag = self.model.country.get_stylized_flag()
        cubes = stylized_flag.get_cube_list()
        for cube in cubes:
            color_name = cube.get_colour_name()
            if color_name != "TRANSPARENT":
                self.model.nextCubeColor = color_name
                break

    def select_frame(self):
        self.model.frame = cv2.VideoCapture(0)
        self.model.worldCamera_is_on = True
