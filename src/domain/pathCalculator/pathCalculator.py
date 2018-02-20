from graph import Graph

class PathCalculator(object):
    MAX_STEP = 10000
    __path = []
    __tableWidth = 20
    __tableHeight = 20
    __defaultWeight = 1
    __tableGraph = Graph()

    def __init__(self):
        for y in range(self.__tableHeight):
            for x in range(self.__tableWidth):
                self.__tableGraph.add_vertex((x, y))

        for y in range(self.__tableHeight):
            for x in range(self.__tableWidth):
                self.__initiate_vertices_neighbors((x, y))

    def __initiate_vertices_neighbors(self, node):
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, -1), (1, -1), (-1, 1), (1, -1)]
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < self.__tableWidth and 0 <= neighbor[1] < self.__tableHeight:
                self.__tableGraph.add_edge(node, neighbor, self.__defaultWeight)

    # startingPoint format: (x,y)
    def calculate_path(self, startingPoint, endPoint):
        processingNode = []
        self.__tableGraph.get_vertex(endPoint).set_step_value(0)
        processingNode.append(endPoint)

        # set_neighbor_step_value
        print("Not empty")
        while processingNode:
            currentNode = processingNode.pop(0)
            for neighbor in self.__tableGraph.get_vertex(currentNode).get_connections():
                if self.__tableGraph.get_vertex(neighbor.get_id()).get_step_value() == -1:
                    self.__tableGraph.get_vertex(neighbor.get_id()).set_step_value(
                        1 + self.__tableGraph.get_vertex(currentNode).get_step_value())
                    processingNode.append(neighbor.get_id())
        print("    empty")

        # find_gluttonous_path
        print("Looking for path")
        step_count = 0
        currentNode = startingPoint
        self.__path.append(currentNode)
        while currentNode != endPoint and step_count < self.MAX_STEP:
            for neighbor in self.__tableGraph.get_vertex(currentNode).get_connections():
                step_count += 1
                if self.__tableGraph.get_vertex(neighbor.get_id()).get_step_value() < \
                        self.__tableGraph.get_vertex(currentNode).get_step_value():
                    self.__path.append(neighbor.get_id())
                    currentNode = neighbor.get_id()

        if currentNode != endPoint:
            print("            path NOT found")
        else:
            print("            path is found")
            self.print_graph_path()
            print("step_count", end=":")
            print(step_count)
        self.print_graph_step()

    def get_graph_path(self):
        return self.__path

    def print_graph_step(self):
        for y in range(self.__tableHeight):
            for x in range(self.__tableWidth):
                print(self.__tableGraph.get_vertex((x, y)).get_step_value(), end=" ")
            print("")

    def print_graph_path(self):
        for node in self.__path:
            print(node)

    def print_graph(self):
        for y in range(self.__tableHeight):
            for x in range(self.__tableWidth):
                print(self.__tableGraph.get_vertex((x, y)).get_id(), end=" Edges::")
                for connection in self.__tableGraph.get_vertex((x, y)).get_connections():
                    print(connection.get_id(), end=' :')
                print()

    # TODO WIP
    # Obstacle
    # Weigth value