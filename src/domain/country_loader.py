class CountryLoader(object):
    def __init__(self):
        self.__country_code_loader()
        self.__stylized_flag_loader()

    def __country_code_loader(self):
        try:
            with open("country\A-Liste_UTF-16.txt", "r", encoding='utf-16') as fileOpen:
                self.country = [l.split() for l in fileOpen.readlines()]
            for x in range(0,196):
                self.country[x][1:len(self.country[x])] = [' '.join(self.country[x][1:len(self.country[x])])]
            fileOpen.close()
        except FileNotFoundError:
            print(' File does NOT exist')

    # TODO WIP
    # def __stylized_flag_loader(self):
        # Discuter a savoir comment géré les nombreuses exceptions (ie Congo, République démocratique -> CongoDM)
        # également si on load avec cv2 les gif et les images vs lodaer les fig et déchiffrer

    def get_country_list(self):
        return self.country