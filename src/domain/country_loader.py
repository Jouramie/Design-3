from PIL import Image

from src.domain.colour import Colour
from src.domain.country import Country
from src.domain.cube import Cube
from src.domain.stylizedFlag import StylizedFlag


class CountryLoader(object):
    def __init__(self, config: dict):
        self.__config = config
        self.__country_dict = {}
        self.__image_max_size = 96
        self.__number_of_pixels_between_two_cubes = 32
        self.__country_code_loader()

    def __country_code_loader(self):
        with open(self.__config['resources_path']['countries_list'], "r", encoding='utf-16') as fileOpen:
            for line in fileOpen:
                line_information = line.split()
                country_code = int(line_information[0])
                country_name = [' '.join(line_information[1:len(line_information)])]
                stylized_flag = self.__stylized_flag_loader(country_name[0])
                country = Country(country_name[0], country_code, stylized_flag)
                self.__country_dict[country_code] = country
            fileOpen.close()

    def __stylized_flag_loader(self, country_name: str):
        image_path: str = self.__config['resources_path']['country_flag'].format(country=country_name)

        pil_gif = Image.open(image_path)
        rgb_im = pil_gif.convert('RGB')
        stylized_flag = StylizedFlag()
        pixel_position_x = 16
        pixel_position_y = 16
        while pixel_position_y <= self.__image_max_size:
            while pixel_position_x <= self.__image_max_size:
                r, g, b = rgb_im.getpixel((pixel_position_x, pixel_position_y))
                for colour in Colour:
                    rgb_colour = colour.value
                    rgb_cube_colour = (r, g, b)
                    if list(rgb_colour) == list(rgb_cube_colour):
                        cube = Cube(colour)
                        stylized_flag.add_cube(cube)
                        pixel_position_x = pixel_position_x + self.__number_of_pixels_between_two_cubes
            pixel_position_x = 16
            pixel_position_y = pixel_position_y + self.__number_of_pixels_between_two_cubes

        return stylized_flag

    def get_country_list(self):
        return self.__country_dict
