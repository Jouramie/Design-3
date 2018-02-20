class Vertex:
    DEFAULT_VALUE = -1
    DEFAULT_WEIGHT = 0

    def __init__(self, node):
        self.__id = node
        self.__adjacent = {}
        self.__stepValue = self.DEFAULT_VALUE

    def add_neighbor(self, neighbor, weight=DEFAULT_WEIGHT):
        self.__adjacent[neighbor] = weight

    def set_new_weight(self, neighbor, weight):
        self.__adjacent[neighbor] = weight

    def set_step_value(self, value):
        self.__stepValue = value

    def get_connections(self):
        return self.__adjacent.keys()

    def get_neighbor_weight(self, neighbor):
        return self.__adjacent[neighbor]

    def get_step_value(self):
        return self.__stepValue

    def get_id(self):
        return self.__id

    def reset_vertex(self):
        self.__stepValue = self.DEFAULT_VALUE
        for connection in self.get_connections():
            self.set_new_weight(connection,self.DEFAULT_WEIGHT)
