from logging import Logger
from unittest import TestCase

from src.d3_network.server_network_controller import MockedServerNetworkController
from src.station.station_controller import StationController
from src.station.station_model import StationModel
from vision.camera import MockedCamera
from vision.coordinate_converter import CoordinateConverter
from vision.robot_detector import MockedRobotDetector
from vision.table_camera_configuration_factory import TableCameraConfigurationFactory

SCENARIO_1 = {

    'config': {
        'table_number': 4,
        'resources_path': {
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
        },
        'camera': {
            'use_mocked_camera': True,
            'mocked_camera_image_path': "fig/saved_images/table2/00h02m31s.jpg",
            'camera_id': 1,
            'image_width': 1600,
            'image_height': 1200,
            'image_save_dir': "fig/{date}"
        },
        'network': {
            'use_mocked_network': True,
            'port': 0
        },
        'robot': {
            'use_mocked_robot_detector': True,
            'update_robot': False

        }
    }
}


class TestScenarioRobotController(TestCase):

    def setUp(self):
        self.logger = Logger("TestScenarioRobotController")
        pass

    def test_scenario1(self):
        # given scenario 1
        station_model, station_controller = self.__create_station_controller(SCENARIO_1)

        # when
        station_controller.update()

        # then
        self.assertIsNotNone(station_model.planned_path)

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

        # TODO configurer le controller et le model

        return station_model, station_controller
