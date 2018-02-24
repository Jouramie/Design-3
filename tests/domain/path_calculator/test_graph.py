from src.domain.path_calculator.graph import Graph

SOME_VALUE_1 = 1
SOME_VALUE_2 = 2
DEFAULT_WEIGHT = 0


def test_when_adding_node_then_add_corresponding_vertex():
    node = (SOME_VALUE_1, SOME_VALUE_2)
    graph = Graph()

    graph.add_vertex(node)

    assert node in graph.get_vertices()


def test_when_adding_edge_then_add_two_ways_connections_between_vertices():
    node_1 = (SOME_VALUE_1, SOME_VALUE_2)
    node_2 = (SOME_VALUE_2, SOME_VALUE_1)
    graph = Graph()
    graph.add_vertex(node_1)
    graph.add_vertex(node_2)

    graph.add_edge(node_1, node_2)

    # Assert connection in both direction
    for value in graph.get_vertex(node_2).get_connections():
        assert node_1 == value.get_id()
    for value in graph.get_vertex(node_1).get_connections():
        assert node_2 == value.get_id()


def test_when_adding_edge_then_add_default_weight():
    node_1 = (SOME_VALUE_1, SOME_VALUE_2)
    node_2 = (SOME_VALUE_2, SOME_VALUE_1)
    graph = Graph()
    graph.add_vertex(node_1)
    graph.add_vertex(node_2)

    graph.add_edge(node_1, node_2)

    # Assert weight in both direction
    assert DEFAULT_WEIGHT == graph.get_vertex(node_1).get_neighbor_weight(graph.get_vertex(node_2))
    assert DEFAULT_WEIGHT == graph.get_vertex(node_2).get_neighbor_weight(graph.get_vertex(node_1))


