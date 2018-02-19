import logging
import os
import time

import cv2

from config import FIG_DIRECTORY, WORLD_CAM_LOG_DIR, WORLD_CAM_LOG_FILE
from src.vision.cameraError import CameraInitializationError, CameraError


class Camera:
    def __init__(self, capture_object, log_level=logging.INFO):
        self.capture_object = capture_object
        self._initialize_log(log_level)

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

    def _initialize_log(self, log_level):
        if not os.path.exists(WORLD_CAM_LOG_DIR):
            os.makedirs(WORLD_CAM_LOG_DIR)

        logging.basicConfig(level=log_level, filename=WORLD_CAM_LOG_FILE, format='%(asctime)s %(message)s')


def create_camera(camera_id):
    capture_object = cv2.VideoCapture(camera_id)
    capture_object.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    capture_object.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    if capture_object.isOpened():
        for i in range(15):
            temp_is_frame_returned, temp_img = capture_object.read()
        logging.info('World cam initialized')
    else:
        logging.info('Camera could not be set properly')
        raise CameraInitializationError('Camera could not be set properly')

    return Camera(capture_object)
