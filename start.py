#!/usr/bin/env python3
# coding: utf-8

import argparse
import logging
import sys
import time

import os
import yaml

import src.d3_network.client_network_controller as client_network_ctl
import src.d3_network.encoder as encoder
import src.d3_network.ip_provider as network_scn
import src.d3_network.server_network_controller as server_network_ctl
import src.robot.robot_controller as robot_ctl
from src.ui.main_app import App


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

    log_file: str = config['log_file'].format(date=time.strftime("%Y-%m-%d-%H:%M:%S"))
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
    network = client_network_ctl.ClientNetworkController(logger.getChild("network_controller"),
                                                         config['network']['port'], encoder.DictionaryEncoder())
    try:
        robot_ctl.RobotController(logger, scanner, network).start()
    except client_network_ctl.socket.timeout as err:
        logger.info(err)
    finally:
        network._socket.close()


def start_station(config: dict, logger: logging.Logger) -> None:
    network_ctl = server_network_ctl.ServerNetworkController(logger.getChild("network_controller"),
                                                             config['network']['port'], encoder.DictionaryEncoder())
    app = App(network_ctl, logger.getChild("main_controller"), config)
    sys.exit(app.exec_())

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
