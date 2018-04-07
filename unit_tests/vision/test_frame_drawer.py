from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

import numpy as np

from src.domain.environments.real_world_environment import RealWorldEnvironment
from src.domain.objects.flag_cube import FlagCube
from src.domain.objects.obstacle import Obstacle
from src.domain.objects.target_zone import TargetZone
from src.domain.environments.vision_environment import VisionEnvironment
from src.domain.objects.color import Color
from src.domain.objects.robot import Robot
from src.domain.objects.vision_cube import VisionCube
from src.vision.frame_drawer import FrameDrawer


class TestFrameDrawer(TestCase):

    def setUp(self):
        self.coordinate_converter = MagicMock()
        self.frame_drawer = FrameDrawer(self.coordinate_converter, MagicMock())

    @patch('src.vision.frame_drawer.cv2')
    def test_when_draw_robot_then_draw_square_orientation_and_radius(self, cv2: Mock):
        robot = Robot((0, 0), 0)
        frame = MagicMock()

        self.frame_drawer.draw_robot(frame, robot)

        cv2.line.assert_called()
        cv2.circle.assert_called()

    @patch('src.vision.frame_drawer.cv2')
    def test_when_draw_vision_environment_then_draw_each_cubes_and_obstacles(self, cv2: Mock):
        cubes = [VisionCube(Color.RED, [(0, 0), (10, 10)]), VisionCube(Color.RED, [(0, 0), (10, 10)])]
        obstacles = [Obstacle((50, 50), 10)]
        vision_environment = VisionEnvironment(cubes, obstacles)
        frame = MagicMock()

        self.frame_drawer.draw_vision_environment(frame, vision_environment)

        cv2.rectangle.assert_called()
        cv2.circle.assert_called()

    @patch('src.vision.frame_drawer.cv2')
    def test_when_draw_real_environment_then_draw_each_cubes_and_obstacles(self, cv2: Mock):
        cubes = [FlagCube((0, 0), Color.BLACK), FlagCube((10, 10), Color.BLUE)]
        obstacles = [Obstacle((50, 50), 10)]
        target_zone = TargetZone(60)
        real_environment = RealWorldEnvironment(obstacles, cubes, target_zone)
        frame = MagicMock()

        self.frame_drawer.draw_real_world_environment(frame, real_environment)

        cv2.rectangle.assert_called()
        cv2.circle.assert_called()

    @patch('src.vision.frame_drawer.cv2')
    def test_when_draw_real_path_then_draw_lines(self, cv2: Mock):
        real_path = [np.array((0, 0, 0), "float32"), np.array((10, 10, 0), "float32"), np.array((10, 20, 0), "float32"),
                     np.array((0, 20, 0), "float32")]
        frame = MagicMock()
        world_points = [[np.array((0, 0, 0), "float32")], [np.array((10, 10, 0), "float32")],
                        [np.array((10, 20, 0), "float32")], [np.array((0, 20, 0), "float32")]]
        self.coordinate_converter.attach_mock(Mock(return_value=world_points), 'project_points_from_real_world_to_pixel')

        self.frame_drawer.draw_real_path(frame, real_path)

        cv2.line.assert_called()

    @patch('src.vision.frame_drawer.cv2')
    def test_when_draw_planned_path_then_draw_lines(self, cv2: Mock):
        planned_path = [((0, 0), (10, 10)), ((10, 10), (10, 20)), ((10, 20), (0, 20))]
        frame = MagicMock()

        self.frame_drawer.draw_planned_path(frame, planned_path)

        cv2.line.assert_called()