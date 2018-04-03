from unittest import TestCase
from src.domain.country_loader import CountryLoader
from src.domain.stylized_flag import StylizedFlag
from src.domain.color import Color
from src.domain.flag_cube import FlagCube

REAL_CONFIG = {'resources_path': {'countries_list': "resources/countries/A-Liste_UTF-16.txt",
                                  'country_flag': "resources/countries/Flag_{country}.gif"}}
EXPECTED_COUNTRY_COUNT = 197
EXPECTED_43_STYLIZED_FLAG = StylizedFlag(
    [FlagCube((5, 61), Color.TRANSPARENT), FlagCube((33, 61), Color.BLUE), FlagCube((61, 61), Color.YELLOW),
     FlagCube((5, 33), Color.TRANSPARENT), FlagCube((33, 33), Color.RED), FlagCube((61, 33), Color.BLUE),
     FlagCube((5, 5), Color.TRANSPARENT), FlagCube((33, 5), Color.BLUE), FlagCube((61, 5), Color.RED)])


class TestCountryLoader(TestCase):
    def test_when_create_country_loader_then_load_all_countries(self):
        country_loader = CountryLoader(REAL_CONFIG)

        self.assertEqual(EXPECTED_COUNTRY_COUNT, len(country_loader._country_dict))

    def test_given_country_code_34_when_get_country_then_return_canada(self):
        country_loader = CountryLoader(REAL_CONFIG)

        country = country_loader.get_country(34)

        self.assertEqual('Canada', country.name)
        self.assertEqual(34, country.code)

    def test_given_country_code_43_when_get_country_then_return_expected_stylized_flag(self):
        country_loader = CountryLoader(REAL_CONFIG)

        country = country_loader.get_country(43)

        self.assertTrue(EXPECTED_43_STYLIZED_FLAG.flag_cubes == country.stylized_flag.flag_cubes)
