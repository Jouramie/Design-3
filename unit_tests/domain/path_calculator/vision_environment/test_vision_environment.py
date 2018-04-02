from unittest import TestCase
from unittest.mock import MagicMock

from src.domain.environments.vision_environment import VisionEnvironment
from src.domain.objects.color import Color
from src.domain.objects.cube import Cube

SOME_COLOR = Color.BLUE
CUBES_OF_ALL_COLORS = [Cube((), Color.BLUE, []), Cube((), Color.WHITE, []), Cube((), Color.RED, []),
                       Cube((), Color.YELLOW, []), Cube((), Color.GREEN, []), Cube((), Color.BLACK, [])]


class TestVisionEnvironment(TestCase):

    def test_given_environment_with_cubes_of_all_colors_when_find_some_color_cube_then_return_cube_of_that_color(self):
        environment = VisionEnvironment(CUBES_OF_ALL_COLORS, [], MagicMock())

        cube = environment.find_cube(SOME_COLOR)

        self.assertEquals(SOME_COLOR, cube.color)
