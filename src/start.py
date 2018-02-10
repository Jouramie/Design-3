import argparse

import robot_software.robot_controller
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
    network = d3_network.network

    robot_software.robot_controller.RobotController(network).start()


def start_station():
    pass


if __name__ == "__main__":
    # execute only if run as a script
    main()
