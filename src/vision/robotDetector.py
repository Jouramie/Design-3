import aruco
import numpy as np

from src.domain.environment.robot import Robot
from src.vision.transform import Transform
from src.vision.coordinateConverter import CoordinateConverter


class RobotDetector:

    def __init__(self, cam_param: aruco.CameraParameters, coordinate_converter: CoordinateConverter):
        self.camParam = cam_param
        self.coordinateConverter = coordinate_converter
        self.detector = aruco.MarkerDetector()
        self.marker_map = aruco.MarkerMap("robot_layout.xml")
        self.marker_tracker = aruco.MarkerMapPoseTracker()
        self.marker_tracker.setParams(self.camParam, self.marker_map)
        self.success = False

    def detect(self, img):
        markers = self.detector.detect(img)
        self.marker_tracker.reset()
        self.success = self.marker_tracker.estimatePose(markers)

        if self.success:
            rvec = self.marker_tracker.getRvec().copy()[0]
            tvec = self.marker_tracker.getTvec().copy()[0]

            camera_to_robot = Transform.from_parameters(np.asscalar(tvec[0]), np.asscalar(tvec[1]),
                                                        np.asscalar(tvec[2]), np.asscalar(rvec[0]),
                                                        np.asscalar(rvec[1]), np.asscalar(rvec[2]))
            world_to_robot = self.coordinateConverter.world_from_camera(camera_to_robot)

            robot_info = world_to_robot.to_parameters(True)
            position_x = robot_info[0]
            position_y = robot_info[1]
            orientation = robot_info[5]

            return Robot((position_x, position_y), orientation)
