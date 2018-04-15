from logging import Logger
from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.d3_network.server_network_controller import MockedServerNetworkController
from src.domain.environments.real_world_environment import RealWorldEnvironment
from src.domain.objects.color import Color
from src.domain.objects.flag_cube import FlagCube
from src.domain.objects.obstacle import Obstacle
from src.station.state import State
from src.station.station_controller import StationController
from src.station.station_model import StationModel
from src.vision.camera import MockedCamera
from src.vision.robot_detector import MockedRobotDetector

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

CUBE_POSITION = {
    'tables': {
        'target_zone': {
            'x': 66.2,
            'y': 66.2
        },
        't2': {
            'cube0': {
                'x': 166.5,
                'y': 84.5,
                'pixel_x': 1360,
                'pixel_y': 240
            },
            'cube1': {
                'x': 180.5,
                'y': 84.5,
                'pixel_x': 1453,
                'pixel_y': 240
            },
            'cube2': {
                'x': 203.5,
                'y': 60.5,
                'pixel_x': 1575,
                'pixel_y': 402
            },
            'cube3': {
                'x': 203.5,
                'y': 46.5,
                'pixel_x': 1575,
                'pixel_y': 501
            },
            'cube4': {
                'x': 203.5,
                'y': 32.5,
                'pixel_x': 1575,
                'pixel_y': 600
            },
            'cube5': {
                'x': 203.5,
                'y': 18.5,
                'pixel_x': 1575,
                'pixel_y': 700
            },
            'cube6': {
                'x': 203.5,
                'y': 4.5,
                'pixel_x': 1575,
                'pixel_y': 800
            },
            'cube7': {
                'x': 180.5,
                'y': -19.5,
                'pixel_x': 1424,
                'pixel_y': 960
            },
            'cube8': {
                'x': 166.5,
                'y': -19.5,
                'pixel_x': 1350,
                'pixel_y': 960
            }
        }
    }
}

SCENARIO_1 = {
    'network_country_code': 31,
    'config': {
        'table_number': 4,
        'resources_path': RESOURCES_PATH,
        'camera': {
            'mocked_camera_image_path': "fig/saved_images/table2/00h02m31s.jpg",
        },
        'robot': {
            'update_robot': False,
            'use_mocked_robot_detector': False,
            'mocked_robot_position': [15, 15],
            'mocked_robot_orientation': 45
        },
        'cube_positions': CUBE_POSITION
    }
}

SCENARIO_2 = {
    'network_country_code': 31,
    'infrared_signal_asked': True,
    'real_world': {
        'cubes': [FlagCube((152, -19), Color.WHITE)],
        'obstacles': [Obstacle((97.45940399169922, 1.5616950988769531), 7)]
    },

    'config': {
        'table_number': 4,
        'resources_path': RESOURCES_PATH,
        'camera': {
            'mocked_camera_image_path': "fig/saved_images/table2/00h02m31s.jpg",
        },
        'robot': {
            'update_robot': False,
            'use_mocked_robot_detector': False,
            'mocked_robot_position': [15, 15],
            'mocked_robot_orientation': 45
        },
        'cube_positions': CUBE_POSITION
    }
}


class TestScenarioStationController(TestCase):

    def setUp(self):
        self.logger = Logger("TestScenarioRobotController")
        pass

    def test_scenario1(self):
        station_model, station_controller = self.__create_station_controller(SCENARIO_1)

        station_controller.update()

        self.assertIs(State.WORKING, station_model.current_state)
        self.assertIs(State.TRAVELING_TO_CUBE_REPOSITORY, station_model.next_state)
        self.assertEqual([((15, 15), (30, 30))], station_model.planned_path)

    def test_scenario2(self):
        station_model, station_controller = self.__create_station_controller(SCENARIO_2)

        station_controller.update()
        station_controller.update()
        station_controller.update()
        station_controller.update()
        station_controller.update()

        self.assertEqual('Burundi', station_model.country.name)
        self.assertEqual('WHITE', station_model.next_cube.color.name)
        self.assertIsNotNone(station_model.planned_path)
        self.assertIs(State.ADJUSTING_IN_FRONT_CUBE_REPOSITORY, station_model.next_state)
        self.assertIs(State.WORKING, station_model.current_state)

    def __create_station_controller(self, scenario: dict) -> (StationModel, StationController):
        station_model = StationModel()
        server_network_controller = MockedServerNetworkController(self.logger, scenario['network_country_code'])

        camera = MockedCamera(scenario['config']['camera']['mocked_camera_image_path'], self.logger)

        real_world = RealWorldEnvironment()
        if 'real_world' in scenario:
            real_world.cubes = scenario['real_world']['cubes']
            real_world.obstacles = scenario['real_world']['obstacles']

        real_world_environment_factory = MagicMock()
        real_world_environment_factory.attach_mock(Mock(return_value=real_world), 'create_real_world_environment')

        robot_detector = MockedRobotDetector(
            (scenario['config']['robot']['mocked_robot_position'][0],
             scenario['config']['robot']['mocked_robot_position'][1]),
            scenario['config']['robot']['mocked_robot_orientation'])

        station_controller = StationController(station_model, server_network_controller, camera,
                                               real_world_environment_factory, robot_detector, self.logger,
                                               scenario['config'])
        station_controller.frame_drawer = MagicMock()

        if 'infrared_signal_asked' in scenario:
            station_model.current_state = State.GETTING_COUNTRY_CODE
            station_model.next_state = None

        station_controller.start_robot()

        return station_model, station_controller
