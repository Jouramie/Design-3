from logging import Logger

from .path_calculator_error import PathCalculatorError, PathCalculatorNoPathError
from .grid import Grid


class PathCalculator(object):
    MAX_ITERATIONS = 20000
    UNASSIGNED_VALUE = -1
    OBSTACLE_VALUE = -2
    STEP_VALUE = 1
    END_POINT_VALUE = 0
    DEFAULT_WEIGHT = 1
    POTENTIAL_WEIGHT = 2
    __path = []

    def __init__(self, logger: Logger):
        self.logger = logger
        self.__last_node = 0
        self.__current_node = 0

    def calculate_path(self, starting_point: tuple, ending_point: tuple, grid: Grid):
        try:
            starting_point = (round(starting_point[0], 0), round(starting_point[1], 0))
            self.__set_grid(grid)
            self.__path.clear()
            self.__set_neighbor_step_value(ending_point)
            self.__validate_path_exist(starting_point)
            return self.__find_gluttonous_path(starting_point, ending_point)
        except PathCalculatorError as grid_err:
            self.logger.info(str(grid_err))
        except PathCalculatorNoPathError as path_err:
            self.logger.info(str(path_err))

    def __set_neighbor_step_value(self, ending_point):
        processing_node = []
        self.__grid.get_vertex(ending_point).set_step_value(self.END_POINT_VALUE)
        processing_node.append(ending_point)

        while processing_node:
            current_node = processing_node.pop(0)
            for connection in self.__grid.get_vertex(current_node).get_connections():
                if self.__grid.get_vertex(connection.get_id()).get_step_value() == self.UNASSIGNED_VALUE:
                    self.__grid.get_vertex(connection.get_id()).set_step_value(
                        self.STEP_VALUE + self.__grid.get_vertex(current_node).get_step_value())
                    processing_node.append(connection.get_id())

    def __find_gluttonous_path(self, starting_point, ending_point):
        iteration_count = 0
        self.__current_node = starting_point
        self.__path.append(self.__current_node)

        while self.__current_node != ending_point and iteration_count < self.MAX_ITERATIONS:
            iteration_count += 1
            self.__find_nodes()

        if self.__current_node != ending_point:
            return False
        else:
            return True

    def __find_nodes(self):
        dangerous_path = False
        gluttonous_path = False
        connection_count = 0
        dangerous_next_node = 0
        safer_next_node = 0
        next_node = 0

        for connection in self.__grid.get_vertex(self.__current_node).get_connections():
            connection_count += 1
            connection_id = connection.get_id()
            neighbor_connection_weight = self.__grid.get_vertex(self.__current_node).get_neighbor_weight(
                self.__grid.get_vertex(connection_id))

            # Section for the next step_value (gluttonous move)
            if self.__grid.get_vertex(connection_id).get_step_value() == self.__grid.get_vertex(
                    self.__current_node).get_step_value() - self.STEP_VALUE:

                # Always go for safe move
                if neighbor_connection_weight == self.DEFAULT_WEIGHT:
                    gluttonous_path = True
                    next_node = connection_id
                # Section for dangerous move
                elif neighbor_connection_weight == self.POTENTIAL_WEIGHT:
                    dangerous_path = True
                    dangerous_next_node = connection_id

            # Section for the same step_value and not turning back
            if connection_id != self.__last_node:
                if self.__grid.get_vertex(connection_id).get_step_value() == self.__grid.get_vertex(
                        self.__current_node).get_step_value():

                    # This move should only be used when is safer then a dangerous move
                    if neighbor_connection_weight == self.DEFAULT_WEIGHT:
                        dangerous_path = True
                        safer_next_node = connection_id

            # Section to set next node (Gluttonous)
            if gluttonous_path:
                self.__add_node_to_path(next_node)
                break
            # Section to set next node (Safety first)
            if connection_count == len(self.__grid.get_vertex(self.__current_node).get_connections()):
                if dangerous_path:
                    if safer_next_node:
                        self.__add_node_to_path(safer_next_node)
                    elif dangerous_next_node:
                        self.__add_node_to_path(dangerous_next_node)

    def __add_node_to_path(self, next_node):
        self.__last_node = self.__path[-1]
        self.__current_node = next_node
        self.__path.append(next_node)

    def __set_grid(self, grid):
        if not grid:
            raise PathCalculatorError("Can't use an empty Grid")
        self.__grid = grid

    def __validate_path_exist(self, starting_point):
        if self.__grid.get_vertex(starting_point).get_step_value() == self.UNASSIGNED_VALUE or \
                self.__grid.get_vertex(starting_point).get_step_value() == self.OBSTACLE_VALUE:
            raise PathCalculatorNoPathError("PathCalculator could not connect start and end point")

    def get_calculated_path(self):
        return self.__path
