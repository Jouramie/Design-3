import logging
import os
import time

import cv2
from src.config import WORLD_CAM_LOG_DIR, WORLD_CAM_LOG_FILE, FIG_DIRECTORY
from src.vision.camera import Camera


class WorldCamera(Camera):
    def __init__(self, camera_id, camera_settings, log_level=logging.INFO):
        self.id = camera_id
        self._initialize_log(log_level)
        self.camera_settings = camera_settings
        self.capture_object = None
        self._initialize()

    def _initialize(self):
        self.capture_object = cv2.VideoCapture(self.id)
        self.capture_object.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
        self.capture_object.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
        if self.capture_object.isOpened():
            for i in range(15):
                temp_is_frame_returned, temp_img = self.capture_object.read()
            logging.info('World cam initialized')
        else:
            logging.error('Camera could not be set properly')

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
            logging.error('No frame was returned while taking a picture')
            return 0

    def _initialize_log(self, log_level):
        if not os.path.exists(WORLD_CAM_LOG_DIR):
            os.makedirs(WORLD_CAM_LOG_DIR)

        logging.basicConfig(level=log_level, filename=WORLD_CAM_LOG_FILE, format='%(asctime)s %(message)s')

