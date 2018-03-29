from src.domain.color import Color


class StylizedFlag(object):

    def __init__(self):
        self.__cube_list = []
        self.colors = []

    def add_color(self, color: Color):
        self.colors.append(color)

    def get_cube_list(self):
        return self.__cube_list
