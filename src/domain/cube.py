class Cube(object):
    def __init__(self, colour):
        self.__colour = colour

    def get_colour_value(self):
        return self.__colour.value

    def get_colour_name(self):
        return self.__colour.name
