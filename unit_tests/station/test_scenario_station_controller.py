from logging import Logger
from unittest import TestCase
from unittest.mock import MagicMock

from src.d3_network.server_network_controller import MockedServerNetworkController
from src.domain.environments.real_world_environment import RealWorldEnvironment
from src.domain.objects.color import Color
from src.domain.objects.cube import Cube
from src.domain.objects.obstacle import Obstacle
from src.station.station_controller import StationController
from src.station.station_model import StationModel
from src.vision.camera import MockedCamera
from src.vision.coordinate_converter import CoordinateConverter
from src.vision.robot_detector import MockedRobotDetector
from src.vision.table_camera_configuration_factory import TableCameraConfigurationFactory

RESOURCES_PATH = {
    'countries_list': "resources/countries/A-Liste_UTF-16.txt",
    'country_flag': "resources/countries/Flag_{country}.gif",
    'camera_calibration':
        ["resources/calibration/table1_2018-03-21.yml",
         "resources/calibration/table2_2018-03-21.yml",
         "resources/calibration/table3_2018-03-21.yml",
         "resources/calibration/table4_2018-03-01.yml",
         "resources/calibration/table5_2018-03-21.yml",
         "resources/calibration/table6_2018-03-21.yml"],
    'world_calibration':
        ["",
         "resources/calibration/world_calibration_2.npy",
         "resources/calibration/world_calibration_3.npy",
         "resources/calibration/world_calibration_4.npy",
         "",
         "resources/calibration/world_calibration_6.npy"]

}

SCENARIO_1 = {
    'config': {
        'table_number': 4,
        'resources_path': RESOURCES_PATH,
        'camera': {
            'mocked_camera_image_path': "fig/saved_images/table2/00h02m31s.jpg",
        },
        'robot': {
            'update_robot': False
        }
    }
}

SCENARIO_2 = {
    'network_country_code': 31,
    'infrared_signal_asked': True,
    'real_world': {
        'cubes': [Cube(Color.WHITE, [(148, -23), (156, -15)])],
        'obstacles': [Obstacle((97.45940399169922, 1.5616950988769531), 7)]
    },

    'config': {
        'table_number': 4,
        'resources_path': RESOURCES_PATH,
        'camera': {
            'mocked_camera_image_path': "fig/saved_images/table2/00h02m31s.jpg",
        },
        'robot': {
            'update_robot': False
        }
    }
}


class TestScenarioStationController(TestCase):

    def setUp(self):
        self.logger = Logger("TestScenarioRobotController")
        pass

    def test_scenario1(self):
        station_model, station_controller = self.__create_station_controller(SCENARIO_1)

        station_controller.update()

        self.assertTrue(station_model.infrared_signal_asked)

    def test_scenario2(self):
        station_model, station_controller = self.__create_station_controller(SCENARIO_2)

        station_controller.update()

        self.assertEqual('Burundi', station_model.country.name)
        self.assertEqual('WHITE', station_model.next_cube.color.name)
        self.assertIsNotNone(station_model.planned_path)
        self.assertTrue(station_model.robot_is_moving)
        self.assertTrue(station_model.robot_is_grabbing_cube)

    def __create_station_controller(self, scenario: dict) -> (StationModel, StationController):
        station_model = StationModel()
        server_network_controller = MockedServerNetworkController(self.logger)

        table_camera_config_factory = TableCameraConfigurationFactory(
            scenario['config']['resources_path']['camera_calibration'],
            scenario['config']['resources_path']['world_calibration'])
        table_camera_config = table_camera_config_factory.create(scenario['config']['table_number'])

        camera = MockedCamera(scenario['config']['camera']['mocked_camera_image_path'], self.logger)
        coordinate_converter = CoordinateConverter(table_camera_config)

        robot_detector = MockedRobotDetector()

        station_controller = StationController(station_model, server_network_controller, camera, coordinate_converter,
                                               robot_detector, self.logger, scenario['config'])
        station_controller.frame_drawer = MagicMock()

        if 'network_country_code' in scenario:
            server_network_controller.COUNTRY_CODE = scenario['network_country_code']
        if 'infrared_signal_asked' in scenario:
            station_model.infrared_signal_asked = scenario['infrared_signal_asked']
        if 'real_world' in scenario:
            real_world = RealWorldEnvironment(MagicMock(), MagicMock())
            real_world.cubes = scenario['real_world']['cubes']
            real_world.obstacles = scenario['real_world']['obstacles']

        station_controller.start_robot()

        return station_model, station_controller
