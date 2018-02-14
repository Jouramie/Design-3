class Vertex:
    def __init__(self, node):
        self.__id = node
        self.__adjacent = {}

    def add_neighbor(self, neighbor, weight=0):
        self.__adjacent[neighbor] = weight

    def set_new_weight(self, neighbor, weight):
        self.__adjacent[neighbor] = weight

    def get_connections(self):
        return self.__adjacent.keys()

    def get_neighbor_weight(self, neighbor):
        return self.__adjacent[neighbor]

    def get_id(self):
        return self.__id