class Cube(object):
    def __init__(self, colour, position):
        self.__colour = colour
        self.__point = position

    def get_colour(self):
        return self.__colour.value

    def get_x_position(self):
        return self.__point.getX()

    def get_y_position(self):
        return self.__point.getY()