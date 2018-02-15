import logging
import os
import platform
import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
from src.config import WORLD_CAM_CALIBRATION_OUTPUT, WORLD_CAM_LOG_DIR, WORLD_CAM_LOG_FILE, FIG_DIRECTORY, \
    WORLD_CAM_CALIBRATION_DIR
from src.vision.camera import Camera


class WorldCamera(Camera):
    def __init__(self, log_level=logging.INFO):
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
        self.camera_matrix = None
        self.distortion_coefs = None

        if not os.path.exists(WORLD_CAM_LOG_DIR):
            os.makedirs(WORLD_CAM_LOG_DIR)

        # TODO set logging level with args at startup
        logging.basicConfig(level=log_level, filename=WORLD_CAM_LOG_FILE, format='%(asctime)s %(message)s')

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
            directory = FIG_DIRECTORY + time.strftime("%Y-%m-%d")

            if not os.path.exists(directory):
                os.makedirs(directory)

            cv2.imwrite(directory + time.strftime("/%Hh%M.jpg"), img)
            return img
        else:
            logging.info('No frame was returned while taking a picture')
            return 0

    def calibrate(self, img_path, inside_corners_in_x, inside_corners_in_y):
        logging.info('Get calibration parameters')
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((inside_corners_in_x * inside_corners_in_y, 3), np.float32)
        objp[:, :2] = np.mgrid[0:inside_corners_in_y, 0:inside_corners_in_x].T.reshape(-1, 2)
        # Arrays to store object points and image points from all the images.
        obj_points = []  # 3d point in real world space
        img_points = []  # 2d points in image plane.

        logging.info('Processing image {}'.format(img_path))
        img = cv2.imread(img_path)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        is_chessboard_found, corners = cv2.findChessboardCorners(gray, (inside_corners_in_x, inside_corners_in_y), None)

        if is_chessboard_found:
            logging.info('Chessboard found')
            img_points.append(corners)
            obj_points.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            cv2.drawChessboardCorners(img, (inside_corners_in_x, inside_corners_in_y), corners2, is_chessboard_found)

            ret, camera_matrix, distortion_coefs, rotation_vectors, translation_vectors = \
                cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

            if not os.path.exists(WORLD_CAM_CALIBRATION_DIR):
                os.makedirs(WORLD_CAM_CALIBRATION_DIR)

            np.savez(WORLD_CAM_CALIBRATION_OUTPUT, ret=ret, camera_matrix=camera_matrix,
                     distortion_coefs=distortion_coefs, rotation_vectors=rotation_vectors,
                     translation_vectors=translation_vectors)
        else:
            logging.info('Chessboard not found')

if __name__ == '__main__':
    world_camera = WorldCamera()
    world_camera.take_picture()
    world_camera.calibrate('../../fig/2018-02-12/09h58.jpg', 7, 7)

