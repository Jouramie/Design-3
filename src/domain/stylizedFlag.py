class StylizedFlag(object):
    def __init__(self):
        self.cubeList = ()

    def addCube(self, cube):
        self.cubeList = self.cubeList + (cube,)

    def getCubeList(self):
        return self.cubeList