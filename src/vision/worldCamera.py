import logging
import os
import platform
import time

import cv2

from src import config
from ..vision.camera import Camera


class WorldCamera(Camera):
    def __init__(self):
        camera_id = None
        system = platform.system()
        if system == 'Linux':
            camera_id = 0
        elif system == 'darwin':
            camera_id = 0
        elif system == 'Windows':
            camera_id = 1
        self.id = camera_id
        self.capture_object = None
        if not os.path.exists(config.WORLD_CAM_LOG_DIR):
            os.makedirs(config.WORLD_CAM_LOG_DIR)
        # TODO set logging level with args at startup
        logging.basicConfig(level=logging.INFO, filename=config.WORLD_CAM_LOG_FILE, format='%(asctime)s %(message)s')
        self._initialize()

    def _initialize(self):
        self.capture_object = cv2.VideoCapture(self.id)
        if self.capture_object.isOpened():
            for i in range(10):
                temp_is_frame_returned, temp_img = self.capture_object.read()
            logging.info('World cam initialized')
        else:
            logging.info('Error, camera could not be set properly')

    def take_picture(self):
        is_frame_returned, img = self.capture_object.read()
        if is_frame_returned:
            logging.info('Picture taken')
            directory = config.FIG_DIRECTORY + time.strftime("%Y-%m-%d")
            if not os.path.exists(directory):
                os.makedirs(directory)
            cv2.imwrite(directory + time.strftime("/%Hh%M.jpg"), img)
            return img
        else:
            logging.info('No frame was returned while taking a picture')
            return 0


if __name__ == '__main__':
    world_camera = WorldCamera()
    world_camera.take_picture()
