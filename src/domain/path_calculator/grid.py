from .direction import Direction
from .vertex import Vertex


class Grid:
    DEFAULT_OFFSET = -23
    DEFAULT_WEIGHT = 1
    UNASSIGNED_VALUE = -1
    OBSTACLE_VALUE = -2
    STEP_VALUE = 1
    END_POINT_VALUE = 0

    def __init__(self, width, height):
        self.__width = width + self.DEFAULT_OFFSET
        self.__height = height + self.DEFAULT_OFFSET
        self.__vertices_dictionary = {}
        self.__number_vertices = 0
        self.__init_grid_vertices()

    def __init_grid_vertices(self):
        for y in range(self.DEFAULT_OFFSET, self.__width + 1):
            for x in range(self.DEFAULT_OFFSET, self.__height + 1):
                self.__add_vertex((x, y))

        for y in range(self.DEFAULT_OFFSET, self.__width + 1):
            for x in range(self.DEFAULT_OFFSET, self.__height + 1):
                self.__initiate_vertices_neighbors((x, y))

    def __add_vertex(self, node):
        self.__number_vertices = self.__number_vertices + 1
        new_vertex = Vertex(node)
        self.__vertices_dictionary[node] = new_vertex
        return new_vertex

    def __initiate_vertices_neighbors(self, node):
        for direction in Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST:
            neighbor = (node[0] + direction.direction[0], node[1] + direction.direction[1])
            if self.DEFAULT_OFFSET <= neighbor[0] < self.__height + 1 and \
                    self.DEFAULT_OFFSET <= neighbor[1] < self.__width + 1:
                self.__add_edge(node, neighbor)

    def __add_edge(self, origin, destination, weight=DEFAULT_WEIGHT):
        self.__vertices_dictionary[origin].add_neighbor(self.__vertices_dictionary[destination], weight)

    def get_vertex(self, node) -> Vertex:
        position = (int(node[0]), int(node[1]))

        if position in self.__vertices_dictionary:
            return self.__vertices_dictionary[position]
        else:
            return None

    def get_vertices(self):
        return self.__vertices_dictionary.keys()

    def reset_neighbor_step_value_keep_obstacles(self, obstacle_value, unassigned_value):
        for y in range(self.DEFAULT_OFFSET, self.__width + 1):
            for x in range(self.DEFAULT_OFFSET, self.__height + 1):
                if self.__vertices_dictionary[(x, y)].get_step_value() != obstacle_value:
                    self.__vertices_dictionary[(x, y)].set_step_value(unassigned_value)

    def is_obstacle(self, point):
        return self.get_vertex(point).get_step_value() == Grid.OBSTACLE_VALUE
