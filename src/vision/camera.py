import os
import time
from logging import Logger
import platform

import cv2

from src.config import FIG_DIRECTORY, ORIGINAL_IMAGE_WIDTH, ORIGINAL_IMAGE_HEIGHT
from src.vision.cameraError import CameraInitializationError, CameraError


class Camera(object):
    def __init__(self, logger: Logger):
        self.logger = logger

    def take_picture(self):
        raise NotImplementedError("This is an interface...")

    def take_video(self):
        raise NotImplementedError("This is an interface...")

    def get_frame(self):
        raise NotImplementedError("This is an interface...")

    def get_fps(self):
        raise NotImplementedError("This is an interface...")

    def release(self):
        raise NotImplementedError("This is an interface...")


class RealCamera(Camera):
    def __init__(self, capture_object, logger: Logger):
        super().__init__(logger)
        self.capture_object = capture_object

    def take_picture(self):
        is_frame_returned, img = self.capture_object.read()
        if is_frame_returned:
            self.logger.info('Picture taken')

            directory = FIG_DIRECTORY + time.strftime("%Y-%m-%d")
            if not os.path.exists(directory):
                os.makedirs(directory)
            cv2.imwrite(directory + time.strftime("/%Hh%Mm%Ss.jpg"), img)

            return img
        else:
            message = 'No frame was returned while taking a picture'
            self.logger.info(message)
            raise CameraError(message)

    def take_video(self):
        while self.capture_object.isOpened():
            ret, frame = self.capture_object.read()
            if ret:
                cv2.imshow('frame', frame)
                if cv2.waitKey(0):
                    break
            else:
                break

    def get_frame(self):
        if self.capture_object.isOpened():
            is_frame_returned = False
            while not is_frame_returned:
                is_frame_returned, frame = self.capture_object.read()
            return frame
        else:
            message = 'Camera is not opened'
            self.logger.info(message)
            raise CameraError(message)

    def get_fps(self):
        if self.capture_object.isOpened():
            fps = self.capture_object.get(cv2.CAP_PROP_FPS)
            return fps
        else:
            message = 'Camera is not opened'
            self.logger.info(message)
            raise CameraError(message)

    def release(self):
        if self.capture_object.isOpened():
            self.logger.info("Capture object released.")
            self.capture_object.release()
        else:
            message = 'Camera is not opened'
            self.logger.info(message)
            raise CameraError(message)


class MockedCamera(Camera):
    def __init__(self, image_file_path: str, logger: Logger):
        super().__init__(logger)
        self.image_file_path = image_file_path

    def take_picture(self):
        return self.get_frame()

    def take_video(self):
        raise NotImplementedError('This method is not implemented yet.')

    def get_frame(self):
        # self.logger.info("Returning image at {}.".format(self.image_file_path))
        return cv2.imread(self.image_file_path)

    def get_fps(self):
        raise NotImplementedError('This method is not implemented yet.')

    def release(self):
        self.logger.info("Capture object released.")


def create_real_camera(camera_id: int, logger: Logger) -> RealCamera:
    capture_object = cv2.VideoCapture(camera_id)
    capture_object.set(cv2.CAP_PROP_FRAME_WIDTH, ORIGINAL_IMAGE_WIDTH)
    capture_object.set(cv2.CAP_PROP_FRAME_HEIGHT, ORIGINAL_IMAGE_HEIGHT)
    if (os == "Windows"):
        # Disable auto-settings of opencv-contrib
        capture_object.set(cv2.CAP_PROP_AUTOFOCUS, False)
        capture_object.set(cv2.CAP_PROP_AUTO_EXPOSURE, False)
        capture_object.set(cv2.CAP_PROP_BACKLIGHT, False)

        # Custum settgins(May need to be modified for Environment colors)
        capture_object.set(cv2.CAP_PROP_BRIGHTNESS, 128)
        capture_object.set(cv2.CAP_PROP_CONTRAST, 25)
        capture_object.set(cv2.CAP_PROP_SATURATION, 28)
        capture_object.set(cv2.CAP_PROP_GAIN, 80)
        capture_object.set(cv2.CAP_PROP_EXPOSURE, 255)
        capture_object.set(cv2.CAP_PROP_TEMPERATURE, 0)
        capture_object.set(cv2.CAP_PROP_ISO_SPEED, 0)
        capture_object.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 0)
        capture_object.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, 0)

        # Set focus
        capture_object.set(cv2.CAP_PROP_FOCUS, 24)
    if (os == "Linux"):
        capture_object.set(cv2.CAP_PROP_CONTRAST, 0.1)
        capture_object.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)


    if capture_object.isOpened():
        logger.info('World cam initialized')
    else:
        raise CameraInitializationError('Camera could not be set properly')

    return RealCamera(capture_object, logger)
