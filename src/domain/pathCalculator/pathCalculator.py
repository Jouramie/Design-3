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
    __width = 20
    __height = 10
    __graph = Graph()

    def __init__(self):
        self.__last_node = 0
        self.__current_node = 0
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

        self.__current_node = starting_point
        self.__path.clear()
        self.__path.append(self.__current_node)

        while self.__current_node != end_point and step_count < self.MAX_STEP:

            dangerous_path = False
            gluttonous_path = False

            last_connection = False
            connection_count = 0

            print("New while", end="")
            print(self.__current_node)

            dangerous_next_node = 0
            safer_next_node = 0
            next_node = 0

            for connection in self.__graph.get_vertex(self.__current_node).get_connections():

                connection_count += 1
                if connection_count == len(self.__graph.get_vertex(self.__current_node).get_connections()):
                    print("Connection Count is the last: ", end="")
                    print(connection_count)
                    last_connection = True

                step_count += 1

                print("New connection", end="")
                print(connection.get_id(), end="")
                print(self.__graph.get_vertex(connection.get_id()).get_step_value())

                # Section for the next step_value (gluttonous move)
                if self.__graph.get_vertex(connection.get_id()).get_step_value() == self.__graph.get_vertex(
                        self.__current_node).get_step_value() - 1:
                    # Always go for safe move
                    if self.__graph.get_vertex(self.__current_node).get_neighbor_weight(
                            self.__graph.get_vertex(connection.get_id())) == self.DEFAULT_WEIGHT:
                        gluttonous_path = True
                        next_node = connection.get_id()
                        print("GLUTTONOUS AND SAFETY FIRST!: ", end="")
                        print(next_node)
                    # Section for dangerous move
                    elif self.__graph.get_vertex(self.__current_node).get_neighbor_weight(
                            self.__graph.get_vertex(connection.get_id())) == self.POTENTIAL_WEIGHT:
                        dangerous_path = True
                        dangerous_next_node = connection.get_id()
                        print("POTENTIAL DANGER!: ", end="")
                        print(dangerous_next_node)

                if self.__last_node:
                    print("last node", end="")
                    print(self.__last_node)
                    print("connection.get_id()", end="")
                    print(connection.get_id())

                # Section for the same step_value and not turning back
                if connection.get_id() != self.__last_node:
                    if self.__graph.get_vertex(connection.get_id()).get_step_value() == self.__graph.get_vertex(
                            self.__current_node).get_step_value():
                        # This move should only be used when is safer then a dangerous move
                        if self.__graph.get_vertex(self.__current_node).get_neighbor_weight(
                                self.__graph.get_vertex(connection.get_id())) == self.DEFAULT_WEIGHT:
                            dangerous_path = True
                            safer_next_node = connection.get_id()
                            print("SAFE ROLLBACK MOVE AVAILABLE: ", end="")
                            print(safer_next_node)

                # Section to set next node (Gluttonous)
                if gluttonous_path:
                    print("A safe journey ahead: ", end="")
                    print(next_node)
                    self.__set_update_nodes(next_node)
                    break
                # Section to set next node (Safety first)
                if last_connection:
                    if dangerous_path:
                        if safer_next_node:
                            print("A safer journey is accessible: ", end="")
                            print(safer_next_node)
                            self.__set_update_nodes(safer_next_node)
                        elif dangerous_next_node:
                            print("A dangerous journey is ahead: ", end="")
                            print(dangerous_next_node)
                            self.__set_update_nodes(dangerous_next_node)

        if self.__current_node != end_point:
            return False
        else:
            return True

    def __set_update_nodes(self, next_node):
        # something else than len(self.__path)-1 ?
        self.__last_node = self.__path[len(self.__path) - 1]
        self.__current_node = next_node
        self.__path.append(next_node)

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