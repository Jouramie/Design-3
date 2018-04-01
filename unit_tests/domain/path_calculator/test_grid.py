from unittest import TestCase

from src.domain.path_calculator.grid import Grid

SOME_DEFAULT_SIZE = 50
SOME_VALUE_0 = 0
SOME_VALUE_1 = 1
SOME_VALUE_2 = 2
SOME_VALUE_3 = 3
DEFAULT_WEIGHT = 1


class TestGrid(TestCase):
    def test_when_creating_grid_then_add_corresponding_vertex(self):
        nodes = [(SOME_VALUE_0, SOME_VALUE_0), (SOME_VALUE_0, SOME_VALUE_1),
                 (SOME_VALUE_1, SOME_VALUE_0), (SOME_VALUE_1, SOME_VALUE_1)]

        grid = Grid(SOME_DEFAULT_SIZE, SOME_DEFAULT_SIZE)

        # Assert all vertices are created
        for node in nodes:
            assert node in grid.get_vertices()

    def test_when_creating_grid_then_add_two_ways_connections_between_vertices(self):
        node_1 = (Grid.DEFAULT_OFFSET, Grid.DEFAULT_OFFSET)
        node_2 = (Grid.DEFAULT_OFFSET, Grid.DEFAULT_OFFSET + 1)

        grid = Grid(SOME_DEFAULT_SIZE, SOME_DEFAULT_SIZE)

        # Assert connection in both direction
        for value in grid.get_vertex(node_2).get_connections():
            assert node_1 == value.get_id()
        for value in grid.get_vertex(node_1).get_connections():
            assert node_2 == value.get_id()

    def test_when_adding_edge_then_add_default_weight(self):
        node_1 = (SOME_VALUE_0, SOME_VALUE_0)
        node_2 = (SOME_VALUE_0, SOME_VALUE_1)

        grid = Grid(SOME_DEFAULT_SIZE, SOME_DEFAULT_SIZE)

        # Assert weight in both direction
        assert DEFAULT_WEIGHT == grid.get_vertex(node_1).get_neighbor_weight(grid.get_vertex(node_2))
        assert DEFAULT_WEIGHT == grid.get_vertex(node_2).get_neighbor_weight(grid.get_vertex(node_1))
