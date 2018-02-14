from .vertex import Vertex

class Graph:
    def __init__(self):
        self.verticesDictionary = {}
        self.numberVertices = 0

    def __iter__(self):
        return iter(self.verticesDictionary.values())

    def add_vertex(self, node):
        self.numberVertices = self.numberVertices + 1
        newVertex = Vertex(node)
        self.verticesDictionary[node] = newVertex
        return newVertex

    def add_edge(self, origin, destination, weight=0):
        if origin not in self.verticesDictionary:
            self.addVertex(origin)
        if destination not in self.verticesDictionary:
            self.addVertex(destination)

        self.verticesDictionary[origin].addNeighbor(self.verticesDictionary[destination], weight)
        self.verticesDictionary[destination].addNeighbor(self.verticesDictionary[origin], weight)

    def get_vertex(self, id):
        if id in self.verticesDictionary:
            return self.verticesDictionary[id]
        else:
            return None

    def get_vertices(self):
        return self.verticesDictionary.keys()