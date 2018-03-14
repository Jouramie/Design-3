import aruco
import cv2
import numpy as np

from src.domain.environment.robot import Robot
from src.vision.transform import Transform


class RobotDetector:

    def __init__(self):
        self.camparam = aruco.CameraParameters()
        self.camparam.readFromXMLFile("../../calibration/table4_2018-03-01.yml")
        self.world_to_camera = Transform.from_matrix(np.load("../../calibration/world_calibration_4.npy"))
        self.detector = aruco.MarkerDetector()

    def detect(self, img):
        markers = self.detector.detect(img)

        for marker in markers:
            if marker.id == 25:
                marker.calculateExtrinsics(16.35, self.camparam, False)
                tvec = marker.Tvec.copy()
                rvec = marker.Rvec.copy()
                camera_to_aruco = Transform.from_parameters(np.asscalar(tvec[0]), np.asscalar(tvec[1]), np.asscalar(tvec[2]), np.asscalar(rvec[0]), np.asscalar(rvec[1]), np.asscalar(rvec[2]))
                world_to_aruco = self.world_to_camera.combine(camera_to_aruco, True)

                robot_info = world_to_aruco.to_parameters(True)
                center_x = robot_info[0]
                center_y = robot_info[1]
                orientation = robot_info[5]

                robot = Robot((center_x, center_y), orientation)

                # 4 corners in world coordinates
                robot_corners = robot.get_corners()

                # Convert from world 3D -> world 2D -> camera -> pixels for drawing
                world_to_aruco_2d = self.world_to_camera.combine(camera_to_aruco, True)
                world_to_aruco_2d.translate(0, 0, -(np.asscalar(robot_info[2])))
                world_2d_to_camera = world_to_aruco.combine(camera_to_aruco.inverse(), True)
                camera_to_world_2d_parameters = world_2d_to_camera.inverse().to_parameters()
                camera_to_world_2d_tvec = np.array([camera_to_world_2d_parameters[0], camera_to_world_2d_parameters[1], camera_to_world_2d_parameters[2]])
                camera_to_world_2d_rvec = np.array([camera_to_world_2d_parameters[3], camera_to_world_2d_parameters[4], camera_to_world_2d_parameters[5]])
                robot_projected_points, jac = cv2.projectPoints(robot_corners, camera_to_world_2d_rvec, camera_to_world_2d_tvec, self.camparam.CameraMatrix, self.camparam.Distorsion)

                # Draw robot
                cv2.line(img, tuple(robot_projected_points[0][0]), tuple(robot_projected_points[1][0]), (204, 0, 204), 3)
                cv2.line(img, tuple(robot_projected_points[1][0]), tuple(robot_projected_points[2][0]), (204, 0, 204), 3)
                cv2.line(img, tuple(robot_projected_points[2][0]), tuple(robot_projected_points[3][0]), (204, 0, 204), 3)
                cv2.line(img, tuple(robot_projected_points[3][0]), tuple(robot_projected_points[0][0]), (204, 0, 204), 3)

                return robot
