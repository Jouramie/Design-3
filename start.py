#!/usr/bin/env python3
# coding: utf-8

import argparse
import logging
import os
import sys
import time

import yaml

import src.d3_network.client_network_controller as client_network_controller
import src.d3_network.encoder as encoder
import src.d3_network.ip_provider as network_scn
import src.d3_network.server_network_controller as server_network_controller
import src.robot.robot_controller as robot_controller
from src.robot.hardware.channel import create_channel
from src.ui.main_app import App
from src.vision.table_camera_configuration_factory import TableCameraConfigurationFactory


def main() -> None:
    parser = argparse.ArgumentParser(description='Script used to start both station or robot.')
    parser.add_argument('sys', choices=['robot', 'station'], help='The system to start, `robot` or `station`.')

    args = parser.parse_args()
    start_system(vars(args))


def start_system(args: dict) -> None:
    logger = logging.getLogger()
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)

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
    logger.info("Config file loaded.\n%s", config)

    if args['sys'] == 'robot':
        start_robot(config['robot'], logger.getChild('robot'))
    elif args['sys'] == 'station':
        start_station(config['station'], logger.getChild('station'))


def start_robot(config: dict, logger: logging.Logger) -> None:
    scanner = network_scn.StaticIpProvider(config['network']['host_ip'])
    network_controller = client_network_controller.ClientNetworkController(logger.getChild("network_controller"),
                                                                           config['network']['port'],
                                                                           encoder.DictionaryEncoder())
    try:
        channel = create_channel(config['serial']['port'])
        robot_controller.RobotController(logger, scanner, network_controller, channel).start()
    finally:
        if network_controller._socket is not None:
            network_controller._socket.close()
        if channel.serial is not None and channel.serial.isOpen:
            channel.serial.close()


def start_station(config: dict, logger: logging.Logger) -> None:
    if config['network']['use_mocked_network']:
        network_controller = server_network_controller.MockedServerNetworkController(
            logger.getChild("network_controller"), config['network']['port'], encoder.Encoder())
    else:
        network_controller = server_network_controller.ServerNetworkController(logger.getChild("network_controller"),
                                                                               config['network']['port'],
                                                                               encoder.DictionaryEncoder())
    table_camera_config_factory = TableCameraConfigurationFactory(config['resources_path']['camera_calibration'],
                                                                  config['resources_path']['world_calibration'])
    table_camera_config = table_camera_config_factory.create(config['table_number'])
    try:
        app = App(network_controller, table_camera_config, logger.getChild("main_controller"), config)
        sys.exit(app.exec_())
    finally:
        if not config['network']['use_mocked_network']:
            if network_controller._server is not None:
                network_controller._server.close()
            if network_controller._socket is not None:
                network_controller._socket.close()


"""
    network_ctl.host_network()
    logger.info("Waiting for robot to connect.")
    station_loop = True
    while station_loop:
        command = input('Type your command: ')

        if command == 'start':
            network_ctl.send_start_command()
        elif command == 'reset':
            network_ctl.send_reset_command()
        elif command == 'quit' or 'exit':
            station_loop = False
        else:
            print('Unknown command.')

"""
if __name__ == "__main__":
    main()
