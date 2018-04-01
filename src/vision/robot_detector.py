import cv2
import numpy as np
from cv2 import aruco

from src.domain.vision_environment.robot import Robot
from src.vision.camera_parameters import CameraParameters
from src.vision.coordinate_converter import CoordinateConverter
from src.vision.transform import Transform


class RobotDetector:

    def __init__(self, cam_param: CameraParameters, coordinate_converter: CoordinateConverter):
        self.cam_param = cam_param
        self.coordinate_converter = coordinate_converter
        self.success = False
        self.marker_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        self.parameters = aruco.DetectorParameters_create()
        points = [np.array([(-10, 10, 0), (-1, 10, 0), (-1, 1, 0), (-10, 1, 0)], 'float32'),
                  np.array([(1, 10, 0), (10, 10, 0), (10, 1, 0), (1, 1, 0)], 'float32'),
                  np.array([(1, -1, 0), (10, -1, 0), (10, -10, 0), (1, -10, 0)], 'float32'),
                  np.array([(-10, 1, 0), (-1, -1, 0), (-1, -10, 0), (-10, -10, 0)], 'float32')]
        ids = np.array([[2], [23], [25], [103]])
        self.board = aruco.Board_create(points, self.marker_dict, ids)

    def detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected_img_points = aruco.detectMarkers(gray, self.marker_dict, parameters=self.parameters,
                                                                cameraMatrix=self.cam_param.camera_matrix,
                                                                distCoeff=self.cam_param.distortion)

        self.success, rotation, translation = aruco.estimatePoseBoard(corners, ids, self.board,
                                                                      self.cam_param.camera_matrix,
                                                                      self.cam_param.distortion)

        if self.success:
            rvec = rotation.copy()
            tvec = translation.copy()

            camera_to_robot = Transform.from_parameters(np.asscalar(tvec[0]), np.asscalar(tvec[1]),
                                                        np.asscalar(tvec[2]), np.asscalar(rvec[0]),
                                                        np.asscalar(rvec[1]), np.asscalar(rvec[2]))
            world_to_robot = self.coordinate_converter.world_from_camera(camera_to_robot)

            robot_info = world_to_robot.to_parameters(True)
            position_x = robot_info[0]
            position_y = robot_info[1]
            orientation = robot_info[5]

            return Robot((position_x, position_y), orientation)
        else:
            return None
