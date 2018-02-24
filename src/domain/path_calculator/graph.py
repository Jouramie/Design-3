from .vertex import Vertex


class Graph:
    DEFAULT_WEIGHT = 0

    def __init__(self):
        self.__vertices_dictionary = {}
        self.__number_vertices = 0

    def add_vertex(self, node):
        self.__number_vertices = self.__number_vertices + 1
        new_vertex = Vertex(node)
        self.__vertices_dictionary[node] = new_vertex
        return new_vertex

    def add_edge(self, origin, destination, weight=DEFAULT_WEIGHT):
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
