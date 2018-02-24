import logging
import os
import time

from .path_calculator.graph import Graph
from .path_calculator.path_calculator import PathCalculator
from .path_calculator.path_calculator_error import PathCalculatorError, PathCalculatorNoPathError
from .environment_error import EnvironmentDataError
from ..config import ENVIRONMENT_LOG_DIR, ENVIRONMENT_LOG_FILE


class Environment(object):
    DEFAULT_SIZE = 5
    DEFAULT_WEIGHT = 1
    POTENTIAL_WEIGHT = 2
    INFINITY_WEIGHT = 3
    OBSTACLE_VALUE = -2

    __width = 0
    __height = 0
    __path_calculator = 0
    __graph = 0
    __obstacles = []
    __infrared_station = 0

    def __init__(self, path_calculator=0, log_level=logging.INFO):
        self.__initialize_log(log_level)
        self.__path_calculator = path_calculator

    def find_path(self, starting_point, ending_point):
        try:
            self.__path_calculator.prepare_neighbor(ending_point)
            self.__path_calculator.calculate_path(starting_point, ending_point)
        except PathCalculatorNoPathError as err:
            logging.info(str(err))

    def initiate_graph(self, width=DEFAULT_SIZE, height=DEFAULT_SIZE, graph=Graph()):
        self.__width = width
        self.__height = height
        self.__graph = graph
        for y in range(self.__height):
            for x in range(self.__width):
                self.__graph.add_vertex((x, y))

        for y in range(self.__height):
            for x in range(self.__width):
                self.__initiate_vertices_neighbors((x, y))

    def initiate_path_calculator(self):
        try:
            self.__path_calculator = PathCalculator(self.__graph)
        except PathCalculatorError as err:
            logging.info(str(err))

    def add_obstacle(self, point):
        try:
            self.__validate_point_in_graph(point)
        except EnvironmentDataError as err:
            logging.info(str(err))
            return False

        self.__graph.get_vertex(point).set_step_value(self.OBSTACLE_VALUE)
        for connection in self.__graph.get_vertex(point).get_connections():
            self.__graph.get_vertex(connection.get_id()).set_new_weight(
                self.__graph.get_vertex(point), self.INFINITY_WEIGHT)
            for connection_decay in self.__graph.get_vertex(connection.get_id()).get_connections():
                if not self.__graph.get_vertex(
                        connection_decay.get_id()).get_step_value() == self.OBSTACLE_VALUE and \
                        not self.__graph.get_vertex(connection.get_id()).get_step_value() == self.OBSTACLE_VALUE:
                    self.__graph.get_vertex(connection_decay.get_id()).set_new_weight(
                        self.__graph.get_vertex(connection.get_id()), self.POTENTIAL_WEIGHT)
        return True

    def __validate_point_in_graph(self, point):
        try:
            self.__graph.get_vertex(point).get_id()
        except AttributeError:
            raise EnvironmentDataError("Invalid point in environment graph")

    def __initiate_vertices_neighbors(self, node):
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, -1), (1, -1), (-1, 1), (1, -1)]
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < self.__width and 0 <= neighbor[1] < self.__height:
                self.__graph.add_edge(node, neighbor, self.DEFAULT_WEIGHT)

    def __initialize_log(self, log_level):
        if not os.path.exists(ENVIRONMENT_LOG_DIR):
            os.makedirs(ENVIRONMENT_LOG_DIR)
        logging.basicConfig(level=log_level, filename=ENVIRONMENT_LOG_FILE, format='%(asctime)s %(message)s')

    def print_graph_path(self):
        for node in self.__path_calculator.get_graph_path():
            logging.info(node)

    def print_graph_steps(self):
        for y in range(self.__height):
            for x in range(self.__width):
                logging.info(self.__graph.get_vertex((x, y)).get_step_value(), end=" ")
            logging.info()

    def print_graph_connections(self):
        for y in range(self.__height):
            for x in range(self.__width):
                logging.info(self.__graph.get_vertex((x, y)).get_id(), end=" Edges::")
                for connection in self.__graph.get_vertex((x, y)).get_connections():
                    logging.info(connection.get_id(), end=" W=")
                    logging.info(self.__graph.get_vertex((x, y)).get_neighbor_weight(
                        self.__graph.get_vertex(connection.get_id())), end=" : ")
                logging.info()

    def reset_to_default(self):
        self.__graph.reset_graph()

