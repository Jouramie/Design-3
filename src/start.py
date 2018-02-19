#!/usr/bin/env python
# coding: utf-8

import argparse
import subprocess

import robot_software.robot_controller as robot_ctl
import d3_network.network_scanner
import d3_network.network


def main():
    parser = argparse.ArgumentParser(description='Script used to start both station or robot.')
    parser.add_argument('sys', choices=['robot', 'station'], help='The system to start, `robot` or `station`.')

    args = parser.parse_args()

    if vars(args)['sys'] == 'robot':
        start_robot()
    elif vars(args)['sys'] == 'station':
        start_station()
    else:
        parser.print_help()


def start_robot():
    # TODO parse config file to create right dependencies
    network_scanner = d3_network.network_scanner
    network = d3_network.network

    robot_ctl.RobotController(network_scanner, network).start()


def start_station():
    subprocess.call("./scripts/boot_robot.bash", shell=True)

    d3_network.network.host_network()


if __name__ == "__main__":
    # execute only if run as a script
    main()
