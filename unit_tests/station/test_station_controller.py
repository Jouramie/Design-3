from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.domain.stylized_flag import StylizedFlag
from src.domain.color import Color
from src.domain.flag_cube import FlagCube

from src.station.station_controller import StationController

EXPECTED_43_STYLIZED_FLAG = StylizedFlag(
    [FlagCube((5, 61), Color.YELLOW), FlagCube((33, 61), Color.BLUE), FlagCube((61, 61), Color.RED),
     FlagCube((5, 33), Color.BLUE), FlagCube((33, 33), Color.RED), FlagCube((61, 33), Color.BLUE),
     FlagCube((5, 5), Color.TRANSPARENT), FlagCube((33, 5), Color.TRANSPARENT), FlagCube((61, 5), Color.TRANSPARENT)])
REAL_CONFIG = {'resources_path': {'countries_list': "resources/countries/A-Liste_UTF-16.txt",
                                  'country_flag': "resources/countries/Flag_{country}.gif"}, 'camera_id': 0}

class TestStationController(TestCase):

    def setUp(self):
        pass

    def test_when_current_flag_index_equal_zero_then_model_next_cube_should_be_first_colored_cube(self):
        station_model = Mock()
        station_model.country.stylized_flag.flag_cubes = EXPECTED_43_STYLIZED_FLAG

        station_controller = StationController(station_model, MagicMock(), MagicMock(), MagicMock(),
                                               REAL_CONFIG)
        station_controller.select_next_cube_color()

        self.assertEqual(EXPECTED_43_STYLIZED_FLAG[0], station_model.next_cube)