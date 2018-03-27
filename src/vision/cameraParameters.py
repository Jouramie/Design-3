import cv2


class CameraParameters:
    def __init__(self, camera_matrix, distortion):
        self.camera_matrix = camera_matrix
        self.distortion = distortion


def create_camera_parameters_from_file(file_path) -> CameraParameters:
    f = cv2.FileStorage(file_path, cv2.FILE_STORAGE_READ)
    camera_matrix = f.getNode("camera_matrix")
    distortion = f.getNode("distortion_coefficients")

    return CameraParameters(camera_matrix.mat(), distortion.mat())

