class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def addNeighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def setNewWeight(self, neighbor, weight):
        self.adjacent[neighbor] = weight

    def getConnections(self):
        return self.adjacent.keys()

    def getNeighborWeight(self, neighbor):
        return self.adjacent[neighbor]

    def getId(self):
        return self.id