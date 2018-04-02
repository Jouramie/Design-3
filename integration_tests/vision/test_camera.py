from unittest import TestCase

from src.vision.camera import *


class TestCamera(TestCase):
    def test_when_video_capture_then_video_is_displayed(self):
        camera = create_real_camera(0)
        camera.take_video()

    def test_when_take_picture_then_picture_saved(self):
        camera = create_real_camera(1)
        camera.take_picture()
