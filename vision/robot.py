import aruco
import numpy as np
from transform import Transform


class RobotDetector:

    def __init__(self):
        self.camparam = aruco.CameraParameters()
        self.camparam.readFromXMLFile("new_calibration4.yml")
        self.world_to_camera = Transform.from_matrix(np.load("world_calibration.npy"))
        #self.marker_config = aruco.MarkerMap("robot_layout.xml")
        #self.marker_tracker = aruco.MarkerMapPoseTracker()
        #self.marker_tracker.setParams(self.camparam, self.marker_config)
        self.detector = aruco.MarkerDetector()
        #self.success = False

    def detect(self, img):
        markers = self.detector.detect(img)
        #self.marker_tracker.reset()
        #self.success = self.marker_tracker.estimatePose(markers)

        for marker in markers:
            marker.draw(img, np.array([255, 255, 255]), 2)
            print("detected id: {}".format(marker.id))
            print("Corners:")
            for i, point in enumerate(marker):
                print("\t{:d} {}".format(i, str(point)))
            marker.calculateExtrinsics(16.35, self.camparam, False)
            tvec = marker.Tvec.copy()
            rvec = marker.Rvec.copy()
            aruco.CvDrawingUtils.draw3dAxis(img, self.camparam, rvec, tvec, 20)
            print("Marker extrinsics:\n{}\n{}".format(tvec, rvec))
            camera_to_aruco = Transform.from_parameters(np.asscalar(tvec[0]), np.asscalar(tvec[1]), np.asscalar(tvec[2]), np.asscalar(rvec[0]), np.asscalar(rvec[1]), np.asscalar(rvec[2]))
            print("Camera->Aruco:\n{}".format(camera_to_aruco))
            world_to_aruco = self.world_to_camera.combine(camera_to_aruco)
            print("World->Aruco:\n{}".format(world_to_aruco))
        #return self.success

    def get_corners(self, marker):
        points = {}
        id = marker.id
        points[id] = []
        for i in range(4):
            points[id].append(marker[i])

        return points