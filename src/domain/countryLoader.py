class CountryLoader(object):

    def countryCodeLoader(self):
        try:
            with open("country\A-Liste_UTF-16.txt", "r", encoding='utf-16') as fileOpen:
                self.country = [l.split() for l in fileOpen.readlines()]
            for x in range(0,196):
                self.country[x][1:len(self.country[x])] = [''.join(self.country[x][1:len(self.country[x])])]
            fileOpen.close()
        except FileNotFoundError:
            print(' File does NOT exist')

    # TODO WIP
    # Load flag in cube with position from .fig
    #def stylizedFlagLoader(self):
        # Pour chaque nom dans self code on cré le flag,
        # Contient des exceptions (ie Congo, République démocratique -> CongoDM)

    def getCountryList(self):
        return self.country