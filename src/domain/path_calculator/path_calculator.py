from logging import Logger

from .direction import Direction
from .grid import Grid
from .path_calculator_error import PathCalculatorError, PathCalculatorNoPathError


class PathCalculator(object):
    MAX_ITERATIONS = 20000
    DEFAULT_WEIGHT = 1
    POTENTIAL_WEIGHT = 2
    __path = []

    def __init__(self, logger: Logger):
        self.logger = logger
        self.__last_node = 0
        self.__current_node = 0
        self.__last_direction = None

    def calculate_path(self, starting_point: tuple, ending_point: tuple, grid: Grid):
        try:
            starting_point = (round(starting_point[0], 0), round(starting_point[1], 0))
            self.__set_grid(grid)
            self.__path.clear()
            self.__reset_neighbor_step_value(ending_point)
            self.__set_neighbor_step_value(ending_point)
            self.__validate_path_exist(starting_point)
            return self.__find_gluttonous_path(starting_point, ending_point)
        except PathCalculatorNoPathError as path_err:
            self.logger.info(str(path_err))
            return False
        except PathCalculatorError as grid_err:
            self.logger.info(str(grid_err))
            return False

    def __reset_neighbor_step_value(self, ending_point):
        if not self.__grid.is_destination(ending_point):
            self.__grid.reset_neighbor_step_value_keep_obstacles(Grid.OBSTACLE_VALUE, Grid.UNASSIGNED_VALUE)

    def __set_neighbor_step_value(self, ending_point):
        processing_node = []
        self.__grid.get_vertex(ending_point).set_step_value(Grid.END_POINT_VALUE)
        processing_node.append(ending_point)

        while processing_node:
            current_node = processing_node.pop(0)
            for connection in self.__grid.get_vertex(current_node).get_connections():
                vertex_direction = (connection.get_id()[0] - current_node[0], connection.get_id()[1] - current_node[1])
                if Direction.find_direction(vertex_direction) in (Direction.NORTH, Direction.SOUTH,
                                                                  Direction.EAST, Direction.WEST):
                    if self.__grid.get_vertex(connection.get_id()).get_step_value() == Grid.UNASSIGNED_VALUE:
                        self.__grid.get_vertex(connection.get_id()).set_step_value(
                            Grid.STEP_VALUE + self.__grid.get_vertex(current_node).get_step_value())
                        processing_node.append(connection.get_id())

    def __find_gluttonous_path(self, starting_point, ending_point):
        iteration_count = 0
        self.__last_node = 0
        self.__last_direction = None
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
        if self.__last_direction is not None:
            fast_track_vertex = (self.__grid.get_vertex(self.__current_node).get_id()[0] + self.__last_direction[0],
                                 self.__grid.get_vertex(self.__current_node).get_id()[1] + self.__last_direction[1])

            if self.__grid.get_vertex(fast_track_vertex).get_step_value() == self.__grid.get_vertex(
                    self.__current_node).get_step_value() - Grid.STEP_VALUE:
                self.__add_node_to_path(fast_track_vertex)
                return

        for connection in self.__grid.get_vertex(self.__current_node).get_connections():
            connection_id = connection.get_id()
            neighbor_connection_weight = self.__grid.get_vertex(self.__current_node).get_neighbor_weight(
                self.__grid.get_vertex(connection_id))

            # Section for the next step_value (gluttonous move)
            if self.__grid.get_vertex(connection_id).get_step_value() == self.__grid.get_vertex(
                    self.__current_node).get_step_value() - Grid.STEP_VALUE:

                # Always go for safe move
                if neighbor_connection_weight == self.DEFAULT_WEIGHT:
                    self.__add_node_to_path(connection_id)
                    return

    def __add_node_to_path(self, next_node):
        self.__last_node = self.__path[-1]
        self.__current_node = next_node
        self.__path.append(next_node)
        self.__last_direction = (self.__current_node[0] - self.__last_node[0],
                                 self.__current_node[1] - self.__last_node[1])

    def __set_grid(self, grid):
        if not grid:
            raise PathCalculatorError("Can't use an empty Grid")
        self.__grid = grid

    def __validate_path_exist(self, starting_point):
        if self.__grid.get_vertex(starting_point).get_step_value() == Grid.UNASSIGNED_VALUE:
            raise PathCalculatorNoPathError("Starting point is not in the grid.")
        elif self.__grid.get_vertex(starting_point).get_step_value() == Grid.OBSTACLE_VALUE:
            raise PathCalculatorNoPathError("Starting point is in an obstacle.")

    def get_calculated_path(self):
        return self.__path
