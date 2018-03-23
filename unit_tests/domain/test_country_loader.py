from unittest import TestCase
from src.domain.country_loader import CountryLoader

REAL_CONFIG = {'resources_path': {'countries_list': "resources/countries/A-Liste_UTF-16.txt",
                                  'country_flag': "resources/countries/Flag_{country}.gif"}}
EXPECTED_COUNTRY_COUNT = 197


class TestCountryLoader(TestCase):
    def test_when_create_country_loader_then_load_all_countries(self):
        country_loader = CountryLoader(REAL_CONFIG)

        self.assertEqual(EXPECTED_COUNTRY_COUNT, len(country_loader._country_dict))

    def test_given_country_code_34_when_get_country_then_return_canada(self):
        country_loader = CountryLoader(REAL_CONFIG)

        country = country_loader.get_country(34)
        self.assertEqual('Canada', country.name)
        self.assertEqual(34, country.code)
        # TODO tester le stylized_flag
