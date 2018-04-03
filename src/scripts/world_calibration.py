import cv2
import cv2.aruco as aruco
import numpy as np
import yaml

from src.vision.camera_parameters import CameraParameters
from src.vision.transform import Transform

if __name__ == '__main__':

    with open("config_world_calibration.yml", "r") as stream:
        config = yaml.load(stream)

    IMAGE_PATH = config["image_path"]
    CAMERA_CALIBRATION = config["camera_calibration"]
    ID = config["id"]
    SIZE = config["size"]
    OUTPUT_FILE = config["output_file"]

    img = cv2.imread(IMAGE_PATH, 1)
    cam_param = create_camera_parameters_from_file(CAMERA_CALIBRATION)
    marker_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
    parameters = aruco.DetectorParameters_create()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, marker_dict, parameters=parameters,
                                                          cameraMatrix=cam_param.camera_matrix,
                                                          distCoeff=cam_param.distortion)
    if len(ids) == 1:
        rvecs, tvecs, objPoints = aruco.estimatePoseSingleMarkers(corners, SIZE, cam_param.camera_matrix,
                                                                  cam_param.distortion)
        tvec = tvecs[0][0]
        rvec = rvecs[0][0]
        half_size = SIZE / 2.0
        tvec[0] = tvec[0] - half_size
        tvec[1] = tvec[1] + half_size
        aruco.drawAxis(img, cam_param.camera_matrix, cam_param.distortion, rvec, tvec, 20)
        camera_to_world = Transform.from_parameters(np.asscalar(tvec[0]), np.asscalar(tvec[1]),
                                                    np.asscalar(tvec[2]), np.asscalar(rvec[0]),
                                                    np.asscalar(rvec[1]), np.asscalar(rvec[2]))

        world_to_camera = camera_to_world.inverse()

        np.save(OUTPUT_FILE, world_to_camera.matrix)

        cv2.imshow('world_calibration', img)
        cv2.waitKey(0)
