from graph import Graph

class PathCalculator(object):
    __defaultWeight = 1
    __tableWidth = 4
    __tableHeight = 3
    __tableGraph = Graph()

    def __init__(self):
        for y in range(self.__tableHeight):
            for x in range(self.__tableWidth):
                self.__tableGraph.add_vertex((x, y))

        for y in range(self.__tableHeight):
            for x in range(self.__tableWidth):
                self.__initiate_vertices_neighbors((x, y))

    def __initiate_vertices_neighbors(self, node):
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < self.__tableWidth and 0 <= neighbor[1] < self.__tableHeight:
                self.__tableGraph.add_edge(node, neighbor, self.__defaultWeight)

    def show_graph(self):
        for y in range(self.__tableHeight):
            for x in range(self.__tableWidth):
                print(self.__tableGraph.get_vertex((x, y)).get_id(), end=" Edges::")
                for connection in self.__tableGraph.get_vertex((x, y)).get_connections():
                    print(connection.get_id(), end=' :')
                print()

    # TODO WIP
    # Obstacle
    # Weigth value