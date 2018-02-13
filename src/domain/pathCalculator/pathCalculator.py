from .graph import Graph

class PathCalculator(object):
    defaultWeight = 1
    tableWidth = 10
    tableHeight = 5
    tableGraph = Graph()

    def __init__(self):
        for y in range(self.tableHeight):
            for x in range(self.tableWidth):
                self.tableGraph.addVertex((x, y))

    # TODO WIP
    #def setVerticesNeighbors(self, node):
        # directions = [[0, -1], [0, 1], [1, 0], [-1, 0]]
        # result = []
        # for direction in directions:
        #   neighbor = [node[0] + direction[0], node[1] + direction[1]]
        #    if 0 <= neighbor[0] < self.tableWidth and 0 <= neighbor[1] < self.tableHeight:
        #        self.tableGraph.addEdge(node, neighbor, self.defaultWeight)
        #        result.append(neighbor)
        # print(node)
        # print(result)

