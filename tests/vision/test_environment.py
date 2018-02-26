from unittest import TestCase
from unittest.mock import MagicMock, Mock

from vision.world_vision import *


class TestEnvironment(TestCase):
    def test_when_creating_environment_then_openCV_called(self):
        capture_object = MagicMock()
        capture_object.attach_mock(Mock(return_value=[True, True]), 'read')

        create_environment(capture_object)

        capture_object.read.assert_called_once()


    def test_when_creating_environment_then_environment_is_returned(self):
        cube_file = '../fig/2018-02-25/17h43.jpg'
        create_environment(cube_file)


    def test_given_cubes_when_creating_environment_then_environment_contains_cubes(self):
        cube_file = '../fig/2018-02-25/17h43.jpg'
        create_environment(cube_file)


    def test_given_obstacles_when_creating_environment_then_environment_contains_obstacles(self):
        obstacle_file = '../fig/2018-02-10/obstacles10.jpg'
        create_environment(cube_file)