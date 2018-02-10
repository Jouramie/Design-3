class Cube(object):

    def __init__(self, colour, position):
        self.colour = colour
        self.point = position

    def getColour(self):
        return self.colour.value

    def getXPosition(self):
        return self.point.getX()

    def getYPosition(self):
        return self.point.getY()