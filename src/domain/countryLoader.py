from PIL import Image

from src.domain.colour import Colour
from src.domain.cube import Cube
from src.domain.stylizedFlag import StylizedFlag
from src.domain.country import Country


class CountryLoader(object):
    def __init__(self):
        self.country_dictionnary = {}
        self.image_max_size = 96
        self.number_of_pixels_between_two_cubes = 32
        self.__country_code_loader()


    def __country_code_loader(self):
        try:
            with open("../domain/countries/A-Liste_UTF-16.txt", "r", encoding='utf-16') as fileOpen:
                for line in fileOpen:
                    line_informations = line.split()
                    country_code = int(line_informations[0])
                    country_name = [' '.join(line_informations[1:len(line_informations)])]
                    stylized_flag = self.__stylized_flag_loader(country_name[0])
                    country = Country(country_name[0], stylized_flag)
                    self.country_dictionnary[country_code] = country
                fileOpen.close()
        except FileNotFoundError:
            print(' File does NOT exist')

    def __stylized_flag_loader(self, country_name):
        pil_gif = Image.open("../domain/countries/Flag_" + country_name + ".gif")
        rgb_im = pil_gif.convert('RGB')
        stylized_flag = StylizedFlag()
        pixel_position_x = 16
        pixel_position_y = 16
        while pixel_position_y <= self.image_max_size:
            while pixel_position_x <= self.image_max_size:
                r, g, b = rgb_im.getpixel((pixel_position_x, pixel_position_y))
                for colour in Colour:
                    rgb_colour = colour.value
                    rgb_cube_colour = (r, g, b)
                    if list(rgb_colour) == list(rgb_cube_colour):
                        cube = Cube(colour)
                        stylized_flag.add_cube(cube)
                        pixel_position_x = pixel_position_x + self.number_of_pixels_between_two_cubes
            pixel_position_x = 16
            pixel_position_y = pixel_position_y + self.number_of_pixels_between_two_cubes

        return stylized_flag

    def get_country_list(self):
        return self.country_dictionnary
