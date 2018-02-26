class StylizedFlag(object):
    def __init__(self):
        self.cubeList = []

    def add_cube(self, cube):
        self.cubeList.append(cube)

    def get_cube_list(self):
        return self.cubeList
