#!/usr/bin/env python3
# coding: utf-8

import argparse
import logging
import os
import sys
import threading
import time

import yaml

import src.d3_network.client_network_controller as client_network_controller
import src.d3_network.encoder as encoder
import src.d3_network.ip_provider as network_scn
import src.d3_network.server_network_controller as server_network_controller
import src.robot.robot_controller as robot_controller
from src.domain.environments.real_world_environment_factory import RealWorldEnvironmentFactory
from src.robot.hardware.channel import create_channel
from src.ui.main_app import App
from src.vision.camera import create_real_camera, MockedCamera
from src.vision.coordinate_converter import CoordinateConverter
from src.vision.frame_drawer import FrameDrawer
from src.vision.robot_detector import MockedRobotDetector, VisionRobotDetector
from src.vision.table_camera_configuration_factory import TableCameraConfigurationFactory


def main() -> None:
    parser = argparse.ArgumentParser(description='Script used to start both station or robot.')
    parser.add_argument('sys', choices=['robot', 'station'], help='The system to start, `robot` or `station`.')

    args = parser.parse_args()
    start_system(vars(args))


def start_system(args: dict) -> None:
    logger = logging.getLogger()
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-7.7s][%(levelname)-5.5s] %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    logger.setLevel(logging.DEBUG)

    with open("resources/config.yml", 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            logger.error("Could not load config file. Exiting.")
            logger.exception(exc)
            return

    if not os.path.exists(config['log_dir']):
        os.makedirs(config['log_dir'])

    log_file: str = config['log_file'].format(date=time.strftime("%Y-%m-%d-%Hh%Mm%Ss"))

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

    if args['sys'] == 'robot':
        start_robot(config['robot'], logger.getChild('robot'))
    elif args['sys'] == 'station':
        start_station(config['station'], logger.getChild('station'))


def start_robot(config: dict, logger: logging.Logger) -> None:
    threading.current_thread().setName('Robot')
    logger.info("Config file loaded.\n%s", config)

    scanner = network_scn.StaticIpProvider(config['network']['host_ip'])
    network_controller = client_network_controller.ClientNetworkController(logger.getChild("network_controller"),
                                                                           config['network']['port'],
                                                                           encoder.DictionaryEncoder())
    try:
        channel = create_channel(config['serial']['port'], logger)
        robot_controller.RobotController(logger, scanner, network_controller, channel).main_loop()
    except Exception as e:
        logger.error(str(e))
    finally:
        if network_controller._socket is not None:
            network_controller._socket.close()
        if channel is not None and channel.serial.isOpen:
            channel.serial.close()


def start_station(config: dict, logger: logging.Logger) -> None:
    threading.current_thread().setName('Station')
    logger.info("Config file loaded.\n%s", config)

    table_camera_config_factory = TableCameraConfigurationFactory(config['resources_path']['camera_calibration'],
                                                                  config['resources_path']['world_calibration'])
    table_camera_config = table_camera_config_factory.create(config['table_number'])

    coordinate_converter = CoordinateConverter(table_camera_config, config['cube_positions']['tables']['t2'])
    if config['robot']['use_mocked_robot_detector']:
        robot_detector = MockedRobotDetector(
            (config['robot']['mocked_robot_position'][0],
             config['robot']['mocked_robot_position'][1]),
            config['robot']['mocked_robot_orientation'])
    else:
        robot_detector = VisionRobotDetector(table_camera_config.camera_parameters, coordinate_converter)

    if config['network']['use_mocked_network']:
        if config['robot']['use_mocked_robot_detector']:
            network_controller = server_network_controller.MockedServerNetworkController(
                logger.getChild("network_controller"), config['network']['mocked_country_code'],
                robot_detector=robot_detector)
        else:
            network_controller = server_network_controller.MockedServerNetworkController(
                logger.getChild("network_controller"), config['network']['mocked_country_code'])
    else:
        network_controller = server_network_controller.SocketServerNetworkController(
            logger.getChild("network_controller"), config['network']['port'], encoder.DictionaryEncoder())

    if config['camera']['use_mocked_camera']:
        camera = MockedCamera(config['camera']['mocked_camera_image_path'], logger.getChild("camera"))
    else:
        camera = create_real_camera(config['camera'], logger.getChild("camera"))

    real_world_environment_factory = RealWorldEnvironmentFactory(coordinate_converter)
    frame_drawer = FrameDrawer(coordinate_converter, logger.getChild("FrameDrawer"))

    try:
        app = App(network_controller, camera, real_world_environment_factory, frame_drawer, robot_detector,
                  logger.getChild("main_controller"),
                  config)
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(str(e))
    finally:
        if not config['network']['use_mocked_network']:
            if network_controller._server is not None:
                network_controller._server.close()
            if network_controller._socket is not None:
                network_controller._socket.close()


if __name__ == "__main__":
    main()
