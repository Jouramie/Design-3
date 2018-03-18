import numpy as np

from src.vision.transform import Transform


class CoordinateConverter:
    def __init__(self):
        self.world_to_camera = Transform.from_matrix(np.load("../../calibration/world_calibration_4.npy"))

    def world_from_camera(self, camera_to_object: Transform):
        return self.world_to_camera.combine(camera_to_object, True)

    def get_world_to_camera(self):
        return self.world_from_camera()

    def get_camera_to_world(self):
        return self.world_to_camera.inverse()
