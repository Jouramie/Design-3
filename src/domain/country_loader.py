from pathlib import Path

from PIL import Image

from src.domain.objects.color import Color
from src.domain.objects.country import Country
from src.domain.objects.stylized_flag import StylizedFlag

IMAGE_MAX_SIZE = 96
NUMBER_OF_PIXELS_BETWEEN_TWO_CUBES = 32


class CountryLoader(object):
    def __init__(self, config: dict):
        self.__config = config
        self._country_dict = {}
        self.__load_countries()

    def __load_countries(self):
        with Path(self.__config['resources_path']['countries_list']).open(encoding='utf-16') as country_file:
            for line in country_file:
                line_content = line.split()
                country_code = int(line_content[0])
                country_name = ' '.join(line_content[1:])
                stylized_flag = self.__load_stylized_country_flag(country_name)
                country = Country(country_name, country_code, stylized_flag)
                self._country_dict[country_code] = country
            country_file.close()

    def __load_stylized_country_flag(self, country_name: str):
        image_path: str = self.__config['resources_path']['country_flag'].format(country=country_name)

        pil_gif = Image.open(Path(image_path))
        rgb_im = pil_gif.convert('RGB')
        colors = []

        pixel_position_x = 16
        pixel_position_y = 16

        while pixel_position_y <= IMAGE_MAX_SIZE:
            while pixel_position_x <= IMAGE_MAX_SIZE:
                rgb = rgb_im.getpixel((pixel_position_x, pixel_position_y))

                color = Color.get_from_rgb(rgb)

                colors.append(color)
                pixel_position_x = pixel_position_x + NUMBER_OF_PIXELS_BETWEEN_TWO_CUBES

            pixel_position_x = 16
            pixel_position_y = pixel_position_y + NUMBER_OF_PIXELS_BETWEEN_TWO_CUBES

        return StylizedFlag(colors)

    def get_country(self, country_code: int) -> Country:
        return self._country_dict[country_code]
