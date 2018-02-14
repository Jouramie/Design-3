from graph import Graph

class PathCalculator(object):
    __defaultWeight = 1
    __tableWidth = 10
    __tableHeight = 5
    __tableGraph = Graph()

    def __init__(self):
        for y in range(self.__tableHeight):
            for x in range(self.__tableWidth):
                self.__tableGraph.add_vertex((x, y))

       # for y in range(self.__tableHeight):
        #    for x in range(self.__tableWidth):
         #       self.__initiate_vertices_neighbors([x, y])

    # TODO WIP
    # def __initiate_vertices_neighbors(self, node):
     #   directions = [[0, -1], [0, 1], [1, 0], [-1, 0]]
     #   result = []
     #   for direction in directions:
     #       neighbor = [node[0] + direction[0], node[1] + direction[1]]
     #       if 0 <= neighbor[0] < self.__tableWidth and 0 <= neighbor[1] < self.__tableHeight:
     #          self.__tableGraph.add_edge(node, neighbor, self.__defaultWeight)
     #          result.append(neighbor)
     #   print(node)
     #   print(result)

    def get_graph(self):
        return self.__tableGraph