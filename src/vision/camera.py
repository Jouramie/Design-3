import logging
import os
import time
import math

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
    capture_object.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
    capture_object.set(cv2.CAP_PROP_CONTRAST, 0.1)

    if capture_object.isOpened():
        logging.info('World cam initialized')
    else:
        logging.info('Camera could not be set properly')
        raise CameraInitializationError('Camera could not be set properly')

    return Camera(capture_object)

if __name__ == '__main__':
    camera = create_camera(2)
    camera.take_picture()