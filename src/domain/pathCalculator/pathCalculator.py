from .graph import Graph

class PathCalculator(object):
    MAX_STEP = 10000
    UNASSIGNED_VALUE = -1
    END_POINT_VALUE = 0
    DEFAULT_WEIGHT = 1
    POTENTIAL_WEIGHT = 2
    __path = []
    __graph = Graph()

    def __init__(self, graph):
        self.__last_node = 0
        self.__current_node = 0
        self.__graph = graph

    def calculate_path(self, starting_point, ending_point):
        self.__path.clear()
        self.__set_neighbor_step_value(ending_point)
        if self.__find_gluttonous_path(starting_point, ending_point):
            return True
        else:
            print("Algo is not good enough")
            # TODO Throw something?
            return False

    def __set_neighbor_step_value(self, ending_point):
        processing_node = []
        self.__graph.get_vertex(ending_point).set_step_value(self.END_POINT_VALUE)
        processing_node.append(ending_point)

        while processing_node:
            current_node = processing_node.pop(0)
            for connection in self.__graph.get_vertex(current_node).get_connections():
                if self.__graph.get_vertex(connection.get_id()).get_step_value() == self.UNASSIGNED_VALUE:
                    self.__graph.get_vertex(connection.get_id()).set_step_value(
                        1 + self.__graph.get_vertex(current_node).get_step_value())
                    processing_node.append(connection.get_id())

    def __find_gluttonous_path(self, starting_point, ending_point):
        if not self.__validate_path_exist(starting_point):
            print("Algo can't find a path")
            return False
            # TODO no path connection between starting and ending

        step_count = 0
        self.__current_node = starting_point
        self.__path.append(self.__current_node)

        while self.__current_node != ending_point and step_count < self.MAX_STEP:
            dangerous_path = False
            gluttonous_path = False
            last_connection = False
            connection_count = 0
            dangerous_next_node = 0
            safer_next_node = 0
            next_node = 0

            for connection in self.__graph.get_vertex(self.__current_node).get_connections():
                connection_count += 1
                if connection_count == len(self.__graph.get_vertex(self.__current_node).get_connections()):
                    last_connection = True

                step_count += 1
                # Section for the next step_value (gluttonous move)
                if self.__graph.get_vertex(connection.get_id()).get_step_value() == self.__graph.get_vertex(
                        self.__current_node).get_step_value() - 1:
                    # Always go for safe move
                    if self.__graph.get_vertex(self.__current_node).get_neighbor_weight(
                            self.__graph.get_vertex(connection.get_id())) == self.DEFAULT_WEIGHT:
                        gluttonous_path = True
                        next_node = connection.get_id()
                    # Section for dangerous move
                    elif self.__graph.get_vertex(self.__current_node).get_neighbor_weight(
                            self.__graph.get_vertex(connection.get_id())) == self.POTENTIAL_WEIGHT:
                        dangerous_path = True
                        dangerous_next_node = connection.get_id()

                # Section for the same step_value and not turning back
                if connection.get_id() != self.__last_node:
                    if self.__graph.get_vertex(connection.get_id()).get_step_value() == self.__graph.get_vertex(
                            self.__current_node).get_step_value():
                        # This move should only be used when is safer then a dangerous move
                        if self.__graph.get_vertex(self.__current_node).get_neighbor_weight(
                                self.__graph.get_vertex(connection.get_id())) == self.DEFAULT_WEIGHT:
                            dangerous_path = True
                            safer_next_node = connection.get_id()

                # Section to set next node (Gluttonous)
                if gluttonous_path:
                    self.__set_update_nodes(next_node)
                    break
                # Section to set next node (Safety first)
                if last_connection:
                    if dangerous_path:
                        if safer_next_node:
                            self.__set_update_nodes(safer_next_node)
                        elif dangerous_next_node:
                            self.__set_update_nodes(dangerous_next_node)

        if self.__current_node != ending_point:
            return False
        else:
            return True

    def __set_update_nodes(self, next_node):
        self.__last_node = self.__path[-1]
        self.__current_node = next_node
        self.__path.append(next_node)

    def __validate_path_exist(self, starting_point):
        if self.__graph.get_vertex(starting_point).get_step_value() == self.UNASSIGNED_VALUE:
            return False
        return True

    def get_graph_path(self):
        if self.__path:
            return self.__path
        else:
            # TODO Throw something?
            print("Please call calculate path first")
            return 0
