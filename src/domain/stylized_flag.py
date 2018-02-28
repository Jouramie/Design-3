class StylizedFlag(object):

    def __init__(self):
        self.__cube_list = ()

    def add_cube(self, cube):
        self.__cube_list = self.__cube_list + (cube,)

    def get_cube_list(self):
        return self.__cube_list
