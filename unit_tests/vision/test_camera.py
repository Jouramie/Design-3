from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.vision.camera import RealCamera
from src.vision.camera_error import CameraError

IMAGE_SAVE_DIRECTORY = "fig/{date}"


class TestRealCamera(TestCase):

    def test_when_successfully_taking_picture_then_openCV_called(self):
        capture_object = MagicMock()
        capture_object.attach_mock(Mock(return_value=[True, True]), 'read')

        camera = RealCamera(capture_object, MagicMock(), IMAGE_SAVE_DIRECTORY)
        camera.take_picture()

        capture_object.read.assert_called_once()

    def test_when_unsuccessfully_taking_a_picture_then_exception_raised(self):
        capture_object = MagicMock()
        capture_object.attach_mock(Mock(return_value=[False, True]), 'read')

        camera = RealCamera(capture_object, MagicMock(), IMAGE_SAVE_DIRECTORY)

        self.assertRaises(CameraError, camera.take_picture)

    def test_when_successfully_taking_a_video_then_openCV_called(self):
        capture_object = MagicMock()
        capture_object.attach_mock(Mock(return_value=[False, True]), 'read')

        camera = RealCamera(capture_object, MagicMock(), IMAGE_SAVE_DIRECTORY)
        camera.take_video()
