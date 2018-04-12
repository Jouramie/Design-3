from unittest import TestCase

from src.domain.path_calculator.grid import Grid

SOME_DEFAULT_SIZE = 60
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

        for node in nodes:
            assert node in grid.get_vertices()

    def test_when_adding_edge_then_add_default_weight(self):
        node_1 = (SOME_VALUE_0, SOME_VALUE_0)
        node_2 = (SOME_VALUE_0, SOME_VALUE_1)

        grid = Grid(SOME_DEFAULT_SIZE, SOME_DEFAULT_SIZE)

        assert DEFAULT_WEIGHT == grid.get_vertex(node_1).get_neighbor_weight(grid.get_vertex(node_2))
        assert DEFAULT_WEIGHT == grid.get_vertex(node_2).get_neighbor_weight(grid.get_vertex(node_1))

    def test_when_resetting_neighbor_then_reset_to_unassigned_value_unless_obstacle(self):
        grid = Grid(SOME_DEFAULT_SIZE, SOME_DEFAULT_SIZE)
        grid.get_vertex((SOME_VALUE_2, SOME_VALUE_2)).set_step_value(Grid.OBSTACLE_VALUE)
        grid.get_vertex((SOME_VALUE_1, SOME_VALUE_1)).set_step_value(SOME_VALUE_3)

        grid.reset_neighbor_step_value_keep_obstacles(Grid.OBSTACLE_VALUE, Grid.UNASSIGNED_VALUE)

        self.assertEqual(Grid.OBSTACLE_VALUE, grid.get_vertex((SOME_VALUE_2, SOME_VALUE_2)).get_step_value())
        self.assertEqual(Grid.UNASSIGNED_VALUE, grid.get_vertex((SOME_VALUE_1, SOME_VALUE_1)).get_step_value())
