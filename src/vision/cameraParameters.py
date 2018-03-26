import cv2


class CameraParameters:
    def __init__(self):
        self.CameraMatrix = None
        self.Distorsion = None

    def readFromFile(self, filePath):
        f = cv2.FileStorage(filePath, cv2.FILE_STORAGE_READ)
        camMatrix = f.getNode("camera_matrix")
        distorsion = f.getNode("distortion_coefficients")
        self.CameraMatrix = camMatrix.mat()
        self.Distorsion = distorsion.mat()

