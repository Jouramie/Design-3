import aruco
import cv2
import numpy as np

from src.domain.environment.robot import Robot
from src.vision.transform import Transform
from src.vision.coordinateConverter import CoordinateConverter


class RobotDetector:

    def __init__(self):
        self.camparam = aruco.CameraParameters()
        self.camparam.readFromXMLFile("../../calibration/table4_2018-03-01.yml")
        self.coordinateConverter = CoordinateConverter()
        self.detector = aruco.MarkerDetector()

    def detect(self, img):
        markers = self.detector.detect(img)

        for marker in markers:
            if marker.id == 25:
                marker.calculateExtrinsics(16.35, self.camparam, False)
                tvec = marker.Tvec.copy()
                rvec = marker.Rvec.copy()
                camera_to_robot = Transform.from_parameters(np.asscalar(tvec[0]), np.asscalar(tvec[1]), np.asscalar(tvec[2]), np.asscalar(rvec[0]), np.asscalar(rvec[1]), np.asscalar(rvec[2]))
                world_to_robot = self.coordinateConverter.world_from_camera(camera_to_robot)

                robot_info = world_to_robot.to_parameters(True)
                center_x = robot_info[0]
                center_y = robot_info[1]
                orientation = robot_info[5]

                robot = Robot((center_x, center_y), orientation)

                # 4 corners in world coordinates
                robot_corners = robot.get_corners()

                # Project corners in image
                camera_to_world_parameters = self.coordinateConverter.get_camera_to_world().to_parameters()
                camera_to_world_tvec = np.array([camera_to_world_parameters[0], camera_to_world_parameters[1], camera_to_world_parameters[2]])
                camera_to_world_rvec = np.array([camera_to_world_parameters[3], camera_to_world_parameters[4], camera_to_world_parameters[5]])
                robot_projected_points, jac = cv2.projectPoints(robot_corners, camera_to_world_rvec, camera_to_world_tvec, self.camparam.CameraMatrix, self.camparam.Distorsion)

                # Draw robot
                cv2.line(img, tuple(robot_projected_points[0][0]), tuple(robot_projected_points[1][0]), (204, 0, 204), 3)
                cv2.line(img, tuple(robot_projected_points[1][0]), tuple(robot_projected_points[2][0]), (204, 0, 204), 3)
                cv2.line(img, tuple(robot_projected_points[2][0]), tuple(robot_projected_points[3][0]), (204, 0, 204), 3)
                cv2.line(img, tuple(robot_projected_points[3][0]), tuple(robot_projected_points[0][0]), (204, 0, 204), 3)

                return robot
