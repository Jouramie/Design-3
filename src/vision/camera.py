import logging
import os
import time

import cv2

from src.config import FIG_DIRECTORY, WORLD_CAM_LOG_DIR, WORLD_CAM_LOG_FILE, ORIGINAL_IMAGE_WIDTH, ORIGINAL_IMAGE_HEIGHT
from src.vision.cameraError import CameraInitializationError, CameraError


class Camera:
    def __init__(self, capture_object, log_level=logging.INFO):
        self.capture_object = capture_object
        #self._initialize_log(log_level)

    def take_picture(self):
        is_frame_returned, img = self.capture_object.read()
        if is_frame_returned:
            logging.info('Picture taken')

            directory = FIG_DIRECTORY + time.strftime("%Y-%m-%d")
            if not os.path.exists(directory):
                os.makedirs(directory)
            cv2.imwrite(directory + time.strftime("/%Hh%Mm%Ss.jpg"), img)

            return img
        else:
            message = 'No frame was returned while taking a picture'
            logging.info(message)
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
            logging.info(message)
            raise CameraError(message)

    def get_fps(self):
        if self.capture_object.isOpened():
            fps = self.capture_object.get(cv2.CAP_PROP_FPS)
            return fps
        else:
            message = 'Camera is not opened'
            logging.info(message)
            raise CameraError(message)

    def release(self):
        if self.capture_object.isOpened():
            self.capture_object.release()
        else:
            message = 'Camera is not opened'
            logging.info(message)
            raise CameraError(message)

    def _initialize_log(self, log_level):
        if not os.path.exists(WORLD_CAM_LOG_DIR):
            os.makedirs(WORLD_CAM_LOG_DIR)

        logging.basicConfig(level=log_level, filename=WORLD_CAM_LOG_FILE, format='%(asctime)s %(message)s')


def create_camera(camera_id):
    capture_object = cv2.VideoCapture(camera_id)
    capture_object.set(cv2.CAP_PROP_FRAME_WIDTH, ORIGINAL_IMAGE_WIDTH)
    capture_object.set(cv2.CAP_PROP_FRAME_HEIGHT, ORIGINAL_IMAGE_HEIGHT)

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

    if capture_object.isOpened():
        logging.info('World cam initialized')
    else:
        logging.info('Camera could not be set properly')
        raise CameraInitializationError('Camera could not be set properly')

    return Camera(capture_object)
