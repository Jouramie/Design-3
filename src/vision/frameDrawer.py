import cv2
import numpy as np

from src.domain.environment.robot import Robot
from src.vision.coordinateConverter import CoordinateConverter
from src.vision.cameraParameters import CameraParameters


class FrameDrawer:
<<<<<<< HEAD
    def __init__(self, cam_param: cv2.aruco.CameraParameters, coordinate_converter: CoordinateConverter):
        self.cam_param = cam_param
        self.coordinate_converter = coordinate_converter
=======
    def __init__(self, cam_param: CameraParameters, coordinate_converter: CoordinateConverter):
        self.camParam = cam_param
        self.coordinateConverter = coordinate_converter
>>>>>>> origin/tracking_robot

    def drawRobot(self, frame, robot: Robot):
        robot_corners = robot.get_corners()

        robot_projected_points = self.__projectPoints(robot_corners)

        cv2.line(frame, tuple(robot_projected_points[0][0]), tuple(robot_projected_points[1][0]), (204, 0, 204), 3)
        cv2.line(frame, tuple(robot_projected_points[1][0]), tuple(robot_projected_points[2][0]), (204, 0, 204), 3)
        cv2.line(frame, tuple(robot_projected_points[2][0]), tuple(robot_projected_points[3][0]), (204, 0, 204), 3)
        cv2.line(frame, tuple(robot_projected_points[3][0]), tuple(robot_projected_points[0][0]), (204, 0, 204), 3)

        return frame

    def __projectPoints(self, points):
        camera_to_world_parameters = self.coordinate_converter.get_camera_to_world().to_parameters()
        camera_to_world_tvec = np.array([camera_to_world_parameters[0], camera_to_world_parameters[1], camera_to_world_parameters[2]])
        camera_to_world_rvec = np.array([camera_to_world_parameters[3], camera_to_world_parameters[4], camera_to_world_parameters[5]])
<<<<<<< HEAD
        projected_points, jac = cv2.projectPoints(points, camera_to_world_rvec, camera_to_world_tvec, self.cam_param.CameraMatrix, self.cam_param.Distorsion)
=======
        projected_points, jac = cv2.projectPoints(points, camera_to_world_rvec, camera_to_world_tvec, self.camParam.CameraMatrix, self.camParam.Distorsion)
>>>>>>> origin/tracking_robot

        return projected_points

    def draw_real_path(self, frame, points):
        i = 0;
        number_of_points = (len(points) - 1)
        while i < number_of_points:
            cv2.line(frame, points[i], points[i + 1], (255, 0, 0), 3)
            i = i + 1

        return frame

    def draw_projected_path(self, frame, points):
        i = 0;
        number_of_points = (len(points) - 1)
        while i < number_of_points:
            cv2.line(frame, points[i], points[i + 1], (0, 255, 0), 3)
            i = i + 1

        return frame
