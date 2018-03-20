import aruco
import cv2
import numpy as np

from src.domain.environment.robot import Robot
from src.vision.transform import Transform
from src.vision.coordinateConverter import CoordinateConverter


class RobotDetector:

    def __init__(self, cam_param: aruco.CameraParameters, coordinate_converter: CoordinateConverter):
        self.camParam = cam_param
        self.coordinateConverter = coordinate_converter
        self.detector = aruco.MarkerDetector()

    def detect(self, img):
        markers = self.detector.detect(img)

        for marker in markers:
            if marker.id == 25:
                marker.calculateExtrinsics(16.35, self.camParam, False)
                tvec = marker.Tvec.copy()
                rvec = marker.Rvec.copy()
                camera_to_robot = Transform.from_parameters(np.asscalar(tvec[0]), np.asscalar(tvec[1]), np.asscalar(tvec[2]), np.asscalar(rvec[0]), np.asscalar(rvec[1]), np.asscalar(rvec[2]))
                world_to_robot = self.coordinateConverter.world_from_camera(camera_to_robot)

                robot_info = world_to_robot.to_parameters(True)
                center_x = robot_info[0]
                center_y = robot_info[1]
                orientation = robot_info[5]

                return Robot((center_x, center_y), orientation)
