import os
import sys
import time
from logging import Logger

import cv2

from src.vision.camera_error import CameraInitializationError, CameraError


class Camera(object):
    def __init__(self, logger: Logger):
        self.logger = logger

    def take_picture(self):
        raise NotImplementedError("This is an interface...")

    def get_frame(self):
        raise NotImplementedError("This is an interface...")

    def get_fps(self):
        raise NotImplementedError("This is an interface...")

    def release(self):
        raise NotImplementedError("This is an interface...")


class RealCamera(Camera):
    def __init__(self, capture_object, logger: Logger, image_save_dir: str):
        super().__init__(logger)
        self.capture_object = capture_object
        self.image_save_dir = image_save_dir

    def take_picture(self):
        self.__check_capture_object_is_opened()
        is_frame_returned, img = self.capture_object.read()
        if is_frame_returned:
            self.logger.info('Picture taken')

            directory = self.image_save_dir.format(date=time.strftime("%Y-%m-%d"))
            if not os.path.exists(directory):
                os.makedirs(directory)
            cv2.imwrite(directory + time.strftime("/%Hh%Mm%Ss.jpg"), img)

            return img
        else:
            message = 'No frame was returned while taking a picture'
            self.logger.info(message)
            raise CameraError(message)

    def get_frame(self):
        self.__check_capture_object_is_opened()
        is_frame_returned = False
        while not is_frame_returned:
            is_frame_returned, frame = self.capture_object.read()
        return frame

    def get_fps(self):
        self.__check_capture_object_is_opened()
        fps = self.capture_object.get(cv2.CAP_PROP_FPS)
        return fps

    def release(self):
        self.__check_capture_object_is_opened()
        self.logger.info("Capture object released.")
        self.capture_object.release()

    def __check_capture_object_is_opened(self):
        if not self.capture_object.isOpened():
            raise CameraError('Camera is not opened')


class MockedCamera(Camera):
    def __init__(self, image_file_path: str, logger: Logger):
        super().__init__(logger)
        self.image_file_path = image_file_path

    def take_picture(self):
        return self.get_frame()

    def get_frame(self):
        # self.logger.info("Returning image at {}.".format(self.image_file_path))
        return cv2.imread(self.image_file_path)

    def get_fps(self):
        raise NotImplementedError('This method is not implemented yet.')

    def release(self):
        self.logger.info("Capture object released.")


def create_real_camera(config: dict, logger: Logger) -> RealCamera:
    capture_object = cv2.VideoCapture(config['camera_id'])
    capture_object.set(cv2.CAP_PROP_FRAME_WIDTH, config['image_width'])
    capture_object.set(cv2.CAP_PROP_FRAME_HEIGHT, config['image_height'])
    print(sys.platform)

    if sys.platform == "win32":
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

    if sys.platform == "linux2":
        capture_object.set(cv2.CAP_PROP_CONTRAST, 0.1)
        capture_object.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)

    if capture_object.isOpened():
        logger.info('World cam initialized')
    else:
        raise CameraInitializationError('Camera could not be set properly')

    return RealCamera(capture_object, logger, config['image_save_dir'])
