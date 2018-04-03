import numpy as np

from src.vision.camera_parameters import *
from src.vision.table_camera_configuration import TableCameraConfiguration
from src.vision.transform import Transform


class TableCameraConfigurationFactory:
    def __init__(self, camera_calibration_path, world_calibration_path):
        self.cam_path = camera_calibration_path
        self.world_calibration_path = world_calibration_path

    def create(self, id):
        if 1 <= id <= 6:
            cam_param = create_camera_parameters_from_file(self.cam_path[id - 1])
            world_to_camera = Transform.from_matrix(np.load(self.world_calibration_path[id - 1]))

            return TableCameraConfiguration(id, cam_param, world_to_camera)
        else:
            raise ValueError("Invalid table number.")
