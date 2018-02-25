import cv2
import numpy as np
from PIL import Image

class CountryLoader(object):
    def __init__(self):
        self.country_dictionnary = {}
        self.__country_code_loader()
        #self.__stylized_flag_loader()

    def __country_code_loader(self):
        try:
            with open("../domain/country/A-Liste_UTF-16.txt", "r", encoding='utf-16') as fileOpen:
                for line in fileOpen:
                    line_informations = line.split()
                    country_code = int(line_informations[0])
                    country_name = [' '.join(line_informations[1:len(line_informations)])]
                    #self.__stylized_flag_loader(country_name[0])
                    self.country_dictionnary[country_code]= country_name
                fileOpen.close()
        except FileNotFoundError:
            print(' File does NOT exist')

    def __stylized_flag_loader(self, country_name):
        #Still working on this...
        pil_gif = Image.open("../domain/country/Flag_" + country_name + ".gif")
        pil_image = Image.new('RGB', pil_gif.size)
        open_cv_image = np.array(pil_image)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        color = open_cv_image[0, 0]
        print(color)

    def get_country_list(self):
        return self.country_dictionnary