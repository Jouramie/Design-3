from path_calculator.graph import Graph
from path_calculator.path_calculator import PathCalculator


class Environment(object):
    # Parameter for environment as a Graph
    WIDTH = 5
    HEIGHT = 5
    DEFAULT_WEIGHT = 1
    POTENTIAL_WEIGHT = 2
    INFINITY_WEIGHT = 3
    OBSTACLE_VALUE = -2

    __path_calculator = 0
    __graph = 0
    # __target_zone = [] undefined
    # __walls = [] define as basic graph outside
    __obstacles = []
    # __cubes = [] define as obstacle for now
    __infrared_station = 0

    #def __init__(self):
        # init environment with photo segmentation

    def initiate_graph(self):
        self.__graph = Graph()
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self.__graph.add_vertex((x, y))

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self.__initiate_vertices_neighbors((x, y))

    def __initiate_vertices_neighbors(self, node):
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, -1), (1, -1), (-1, 1), (1, -1)]
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < self.WIDTH and 0 <= neighbor[1] < self.HEIGHT:
                self.__graph.add_edge(node, neighbor, self.DEFAULT_WEIGHT)

    def initiate_path_calculator(self):
        self.__path_calculator = PathCalculator(self.__graph)
        # TODO add some catch to assure graph is ok first

    def add_obstacle(self, point):
        self.__graph.get_vertex(point).set_step_value(self.OBSTACLE_VALUE)
        for connection in self.__graph.get_vertex(point).get_connections():
            self.__graph.get_vertex(connection.get_id()).set_new_weight(
                self.__graph.get_vertex(point), self.INFINITY_WEIGHT)
            for connection_decay in self.__graph.get_vertex(connection.get_id()).get_connections():
                if not self.__graph.get_vertex(
                        connection_decay.get_id()).get_step_value() == self.OBSTACLE_VALUE and \
                        not self.__graph.get_vertex(connection.get_id()).get_step_value() == self.OBSTACLE_VALUE:
                    self.__graph.get_vertex(connection_decay.get_id()).set_new_weight(
                        self.__graph.get_vertex(connection.get_id()), self.POTENTIAL_WEIGHT)

    def calculate_path(self, starting_point, ending_point):
        if self.__path_calculator.calculate_path(starting_point, ending_point):
            return True
        else:
            return False

    def print_graph_path(self):
        if self.__path_calculator.get_graph_path():
            for node in self.__path_calculator.get_graph_path():
                print(node)
        else:
            print("No graph to show")

    def print_graph_connections(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                print(self.__graph.get_vertex((x, y)).get_id(), end=" Edges::")
                for connection in self.__graph.get_vertex((x, y)).get_connections():
                    print(connection.get_id(), end=" W=")
                    print(self.__graph.get_vertex((x, y)).get_neighbor_weight(
                        self.__graph.get_vertex(connection.get_id())), end=" : ")
                print()

    def print_graph_steps(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                print(self.__graph.get_vertex((x, y)).get_step_value(), end=" ")
            print()

    # This reset graph to default connections and empty environment
    def reset_to_default(self):
        self.__graph.reset_graph()

