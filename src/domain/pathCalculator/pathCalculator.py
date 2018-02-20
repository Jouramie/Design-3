#TODO move environment and graph creation logic out of here
from graph import Graph

class PathCalculator(object):
    MAX_STEP = 10000
    OBSTACLE_VALUE = -2
    END_POINT_VALUE = 0
    DEFAULT_WEIGHT = 1
    POTENTIAL_WEIGHT = 2
    INFINITY_WEIGHT = 3
    __path = []
    __width = 5
    __height = 5
    __graph = Graph()

    def __init__(self):
        for y in range(self.__height):
            for x in range(self.__width):
                self.__graph.add_vertex((x, y))

        for y in range(self.__height):
            for x in range(self.__width):
                self.__initiate_vertices_neighbors((x, y))

    def __initiate_vertices_neighbors(self, node):
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0), (-1, -1), (1, -1), (-1, 1), (1, -1)]
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < self.__width and 0 <= neighbor[1] < self.__height:
                self.__graph.add_edge(node, neighbor, self.DEFAULT_WEIGHT)

    # (starting/end)_point format: (x,y)
    def calculate_path(self, starting_point, end_point):
        self.__set_neighbor_step_value(end_point)
        if self.__find_gluttonous_path(starting_point, end_point):
            self.print_graph_path()
        else:
            print("Algo is not good enough")
        self.print_graph_steps()

    def __set_neighbor_step_value(self, end_point):
        processing_node = []
        self.__graph.get_vertex(end_point).set_step_value(self.END_POINT_VALUE)
        processing_node.append(end_point)

        # set_neighbor_step_value
        while processing_node:
            current_node = processing_node.pop(0)
            for connection in self.__graph.get_vertex(current_node).get_connections():
                if self.__graph.get_vertex(connection.get_id()).get_step_value() == -1:
                    self.__graph.get_vertex(connection.get_id()).set_step_value(
                        1 + self.__graph.get_vertex(current_node).get_step_value())
                    processing_node.append(connection.get_id())

    def __find_gluttonous_path(self, starting_point, end_point):
        step_count = 0
        dangerous_path = False
        self.__path.clear()
        current_node = starting_point
        self.__path.append(current_node)
        while current_node != end_point and step_count < self.MAX_STEP:
            for connection in self.__graph.get_vertex(current_node).get_connections():
                step_count += 1
                dangerous_path = False
                potential_next_node = ()
                if self.__graph.get_vertex(connection.get_id()).get_step_value() == \
                        self.__graph.get_vertex(current_node).get_step_value() - 1:
                    potential_next_node = connection.get_id()
                    print(potential_next_node)
                    #TODO FIX THIS
                    if self.__graph.get_vertex(current_node).get_neighbor_weight(connection.get_id()) == \
                            self.POTENTIAL_WEIGHT:
                        dangerous_path = True
                        print("Potentially Dangerous Path Detected")
                    else:
                        dangerous_path = False
                        print("Safe Path Found")
                if dangerous_path:
                    print("Dangerous Path Adjustment")
                    if self.__graph.get_vertex(connection.get_id()).get_step_value() == \
                            self.__graph.get_vertex(current_node).get_step_value() and \
                            self.__graph.get_vertex(current_node).get_neighbor_weight(
                                self.__graph.get_vertex(potential_next_node)) == self.DEFAULT_WEIGHT:
                        print("DPA Successful")
                        current_node = connection.get_id()
                    else:
                        print("DPA Fail")
                        current_node = potential_next_node
                else:
                    current_node = connection.get_id()
                self.__path.append(current_node)


        if current_node != end_point:
            return False
        else:
            return True

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

    def get_graph_path(self):
        return self.__path

    def print_graph_steps(self):
        for y in range(self.__height):
            for x in range(self.__width):
                print(self.__graph.get_vertex((x, y)).get_step_value(), end=" ")
            print("")

    def print_graph_path(self):
        for node in self.__path:
            print(node)

    def print_graph_edges(self):
        for y in range(self.__height):
            for x in range(self.__width):
                print(self.__graph.get_vertex((x, y)).get_id(), end=" Edges::")
                for connection in self.__graph.get_vertex((x, y)).get_connections():
                    print(connection.get_id(), end=' W=')
                    print(self.__graph.get_vertex((x, y)).get_neighbor_weight(
                        self.__graph.get_vertex(connection.get_id())), end=' : ')
                print()

    def reset_graph_to_default(self):
        self.__graph.reset_graph()

    # TODO WIP
    # Weigth value