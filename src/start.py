#!/usr/bin/env python
# coding: utf-8

import argparse
import subprocess
import yaml

import robot_software.robot_controller as robot_ctl
import d3_network.network_scanner as network_scn
import d3_network.network_controller as network_ctl


def main():
    parser = argparse.ArgumentParser(description='Script used to start both station or robot.')
    parser.add_argument('sys', choices=['robot', 'station'], help='The system to start, `robot` or `station`.')

    args = parser.parse_args()

    with open("config.yml", 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            # TODO print in logger
            print("Could not load config file. Exiting.")
            print(exc)
            return

    # TODO print in logger
    print(config)

    if vars(args)['sys'] == 'robot':
        start_robot(config['robot'])
    elif vars(args)['sys'] == 'station':
        start_station(config['station'])
    else:
        parser.print_help()


def start_robot(config):
    # TODO parse config file to create right dependencies
    if config['network']['scan_for_ip']:
        scanner = network_scn.NmapNetworkScanner()
    else:
        scanner = network_scn.StaticNetworkScanner(config['network']['host_ip'])
    network = network_ctl.NetworkController(config['network']['port'])

    robot_ctl.RobotController(scanner, network).start()


def start_station(config):
    if not config['simulated_robot']:
        subprocess.call("./scripts/boot_robot.bash", shell=True)

    print("waiting for robot to connect")

    network_ctl.NetworkController(config['network']['port']).host_network()


if __name__ == "__main__":
    main()
