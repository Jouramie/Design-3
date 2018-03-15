from .vertex import Vertex
from src.domain.path_calculator.direction import Direction


class Grid:
    DEFAULT_WEIGHT = 1

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__vertices_dictionary = {}
        self.__number_vertices = 0
        self.__init_grid_vertices()

    def __init_grid_vertices(self):
        for y in range(self.__height):
            for x in range(self.__width):
                self.__add_vertex((x, y))

        for y in range(self.__height):
            for x in range(self.__width):
                self.__initiate_vertices_neighbors((x, y))

    def __add_vertex(self, node):
        self.__number_vertices = self.__number_vertices + 1
        new_vertex = Vertex(node)
        self.__vertices_dictionary[node] = new_vertex
        return new_vertex

    def __initiate_vertices_neighbors(self, node):
        for direction in Direction:
            neighbor = (node[0] + direction.value[0], node[1] + direction.value[1])
            if 0 <= neighbor[0] < self.__width and 0 <= neighbor[1] < self.__height:
                self.__add_edge(node, neighbor)

    def __add_edge(self, origin, destination, weight=DEFAULT_WEIGHT):
        self.__vertices_dictionary[origin].add_neighbor(self.__vertices_dictionary[destination], weight)
        self.__vertices_dictionary[destination].add_neighbor(self.__vertices_dictionary[origin], weight)

    def get_vertex(self, node):
        if node in self.__vertices_dictionary:
            return self.__vertices_dictionary[node]
        else:
            return None

    def get_vertices(self):
        return self.__vertices_dictionary.keys()

    def reset_graph(self):
        for vertex in self.__vertices_dictionary.values():
            vertex.reset_vertex()
