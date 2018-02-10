class Country(object):

    def __init__(self, name, code, stylizedFlag):
        self.name = name
        self.code = code
        self.stylizedFlag = stylizedFlag

    def getCountryName(self):
        return self.name

    def getCountryCode(self):
        return self.code

    def getStylizedFlag(self):
        return self.stylizedFlag