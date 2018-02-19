from vertex import Vertex

class Graph:
    def __init__(self):
        self.__verticesDictionary = {}
        self.__numberVertices = 0

    def __iter__(self):
        return iter(self.__verticesDictionary.values())

    def add_vertex(self, node):
        self.__numberVertices = self.__numberVertices + 1
        new_vertex = Vertex(node)
        self.__verticesDictionary[node] = new_vertex
        return new_vertex

    def add_edge(self, origin, destination, weight=0):
        self.__verticesDictionary[origin].add_neighbor(self.__verticesDictionary[destination], weight)
        self.__verticesDictionary[destination].add_neighbor(self.__verticesDictionary[origin], weight)

    def get_vertex(self, node):
        if node in self.__verticesDictionary:
            return self.__verticesDictionary[node]
        else:
            return None

    def get_vertices(self):
        return self.__verticesDictionary.keys()