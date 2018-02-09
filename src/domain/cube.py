
class Cube(object):

    def __init__(self, colour, position):
        self.Colour = colour
        self.Point = position

    def getColour(self):
        return self.Colour.value

    def getXPosition(self):
        return self.Point.getX()

    def getYPosition(self):
        return self.Point.getY()