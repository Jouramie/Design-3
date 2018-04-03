from unittest import TestCase
from unittest.mock import MagicMock

from src.vision.camera import create_real_camera

config = {'camera_id': 1, 'image_width': 1600, 'image_height': 1200}


class TestRealCamera(TestCase):
    def test_when_video_capture_then_video_is_displayed(self):
        camera = create_real_camera(config, MagicMock())
        camera.take_video()

    def test_when_take_picture_then_picture_saved(self):
        camera = create_real_camera(config, MagicMock())
        camera.take_picture()
