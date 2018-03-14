import aruco
import cv2
import numpy as np

from transform import Transform
from math import cos, sin, radians


class RobotDetector:

    def __init__(self):
        self.camparam = aruco.CameraParameters()
        self.camparam.readFromXMLFile("../../calibration/table4_2018-03-01.yml")
        self.world_to_camera = Transform.from_matrix(np.load("../../calibration/world_calibration_4.npy"))
        self.detector = aruco.MarkerDetector()
        self.success = False

    def detect(self, img):
        self.success = False;
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
                print("===== 3D =====")
                print("Position : ({}, {})".format(center_x, center_y))
                print("Orientation : {}°".format(orientation))

                #Debug Height
                print("Hauteur : {}".format(robot_info[2]))

                world_to_aruco_2d = self.world_to_camera.combine(camera_to_aruco, True)
                world_to_aruco_2d.translate(0, 0, -(np.asscalar(robot_info[2])))
                robot_info_2d = world_to_aruco_2d.to_parameters(True)
                center_x_2d = robot_info_2d[0]
                center_y_2d = robot_info_2d[1]
                orientation_2d = radians(robot_info_2d[5])
                print("===== 2D =====")
                print("Position : ({}, {})".format(center_x_2d, center_y_2d))
                print("Orientation : {}°".format(robot_info_2d[5]))
                # Debug Height
                print("Hauteur : {}".format(robot_info_2d[2]))

                offset_top_left_x = -8.175
                offset_top_left_y = 8.175
                top_left_x = center_x_2d + (offset_top_left_x * cos(orientation_2d)) - (offset_top_left_y * sin(orientation_2d))
                top_left_y = center_y_2d + (offset_top_left_x * sin(orientation_2d)) + (offset_top_left_y * cos(orientation_2d))
                top_left = [top_left_x, top_left_y, 0]

                offset_top_right_x = 8.175
                offset_top_right_y = 8.175
                top_right_x = center_x_2d + (offset_top_right_x * cos(orientation_2d)) - (offset_top_right_y * sin(orientation_2d))
                top_right_y = center_y_2d + (offset_top_right_x * sin(orientation_2d)) + (offset_top_right_y * cos(orientation_2d))
                top_right = [top_right_x, top_right_y, 0]

                offset_bot_right_x = 8.175
                offset_bot_right_y = -8.175
                bot_right_x = center_x_2d + (offset_bot_right_x * cos(orientation_2d)) - (offset_bot_right_y * sin(orientation_2d))
                bot_right_y = center_y_2d + (offset_bot_right_x * sin(orientation_2d)) + (offset_bot_right_y * cos(orientation_2d))
                bot_right = [bot_right_x, bot_right_y, 0]

                offset_bot_left_x = -8.175
                offset_bot_left_y = -8.175
                bot_left_x = center_x_2d + (offset_bot_left_x * cos(orientation_2d)) - (offset_bot_left_y * sin(orientation_2d))
                bot_left_y = center_y_2d + (offset_bot_left_x * sin(orientation_2d)) + (offset_bot_left_y * cos(orientation_2d))
                bot_left = [bot_left_x, bot_left_y, 0]

                robot_points = np.float32([top_left, top_right, bot_right, bot_left]).reshape(-1, 3)

                world_2d_to_camera = world_to_aruco.combine(camera_to_aruco.inverse(), True)

                camera_to_world_2d_parameters = world_2d_to_camera.inverse().to_parameters()
                camera_to_world_2d_tvec = np.array([camera_to_world_2d_parameters[0], camera_to_world_2d_parameters[1], camera_to_world_2d_parameters[2]])
                camera_to_world_2d_rvec = np.array([camera_to_world_2d_parameters[3], camera_to_world_2d_parameters[4], camera_to_world_2d_parameters[5]])
                robot_projected_points, jac = cv2.projectPoints(robot_points, camera_to_world_2d_rvec, camera_to_world_2d_tvec, self.camparam.CameraMatrix, self.camparam.Distorsion)

                cv2.line(img, tuple(robot_projected_points[0][0]), tuple(robot_projected_points[1][0]), (204, 0, 204), 3)
                cv2.line(img, tuple(robot_projected_points[1][0]), tuple(robot_projected_points[2][0]), (204, 0, 204), 3)
                cv2.line(img, tuple(robot_projected_points[2][0]), tuple(robot_projected_points[3][0]), (204, 0, 204), 3)
                cv2.line(img, tuple(robot_projected_points[3][0]), tuple(robot_projected_points[0][0]), (204, 0, 204), 3)

                self.success = True;

        return self.success