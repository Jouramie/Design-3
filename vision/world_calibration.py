import aruco
import cv2
import yaml
import numpy as np

from transform import Transform

if __name__ == '__main__':

    with open("config_world_calibration.yml", "r") as stream:
        config = yaml.load(stream)

    IMAGE_PATH = config["image_path"]
    CAMERA_CALIBRATION = config["camera_calibration"]
    ID = config["id"]
    SIZE = config["size"]
    OUTPUT_FILE = config["output_file"]

    img = cv2.imread(IMAGE_PATH, 1)
    camparam = aruco.CameraParameters()
    camparam.readFromXMLFile(CAMERA_CALIBRATION)
    detector = aruco.MarkerDetector()
    markers = detector.detect(img)
    for marker in markers:
        if marker.id == ID:
            marker.calculateExtrinsics(SIZE, camparam, False)
            tvec = marker.Tvec.copy()
            rvec = marker.Rvec.copy()
            half_size = SIZE/2.0
            tvec[0] = tvec[0] - half_size
            tvec[1] = tvec[1] + half_size
            aruco.CvDrawingUtils.draw3dAxis(img, camparam, rvec, tvec, 20)
            camera_to_world = Transform.from_parameters(np.asscalar(tvec[0]), np.asscalar(tvec[1]),
                                                        np.asscalar(tvec[2]), np.asscalar(rvec[0]),
                                                        np.asscalar(rvec[1]), np.asscalar(rvec[2]))

            world_to_camera = camera_to_world.inverse()

            np.save(OUTPUT_FILE, world_to_camera.matrix)

            cv2.imshow('world_calibration', img)
            cv2.waitKey(0)

