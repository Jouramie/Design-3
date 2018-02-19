from unittest import TestCase
from unittest.mock import MagicMock, Mock

from src.vision.camera import Camera
from src.vision.cameraError import CameraError


class TestCamera(TestCase):

    def test_when_successfully_taking_picture_then_openCV_called(self):
        capture_object = MagicMock()
        capture_object.attach_mock(Mock(return_value=[True, True]), 'read')

        camera = Camera(capture_object)
        camera.take_picture()

        capture_object.read.assert_called_once()

    def test_when_unsuccessfully_taking_a_picture_then_exception_raised(self):
        capture_object = MagicMock()
        capture_object.attach_mock(Mock(return_value=[False, True]), 'read')

        camera = Camera(capture_object)

        self.assertRaises(CameraError, camera.take_picture)




