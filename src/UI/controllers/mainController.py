import cv2


class MainController(object):
    def __init__(self, model):
        self.model = model

    def start_timer(self):
        self.model.timer.start(1000)
        print("start timer")

    def select_flag(self):
        self.model.flag = "Allemagne"

    def select_country_name(self):
        self.model.countryName = "Allemagne"

    def select_next_cube_color(self):
        self.model.nextCubeColor = "black"

    def select_frame(self):
        self.model.frame = cv2.VideoCapture(0)
        self.model.worldCamTimer.start(1)
