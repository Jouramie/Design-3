class Country(object):

    def __init__(self, name, code, stylizedFlag):
        self.__name = name
        self.__code = code
        self.__stylizedFlag = stylizedFlag

    def get_country_name(self):
        return self.__name

    def get_country_code(self):
        return self.__code

    def get_stylized_flag(self):
        return self.__stylizedflag