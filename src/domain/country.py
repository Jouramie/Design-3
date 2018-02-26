class Country(object):
    def __init__(self, name, stylized_flag):
        self.__name = name
        self.__stylizedFlag = stylized_flag

    def get_country_name(self):
        return self.__name

    def get_stylized_flag(self):
        return self.__stylizedFlag
