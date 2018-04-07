import numpy as np

from src.vision.camera_parameters import *
from src.vision.table_camera_configuration import TableCameraConfiguration
from src.vision.transform import Transform


class TableCameraConfigurationFactory:
    def __init__(self, camera_calibration_path, world_calibration_path):
        self.cam_path = camera_calibration_path
        self.world_calibration_path = world_calibration_path

    def create(self, table_number):
        if 1 <= table_number <= 6:
            cam_param = create_camera_parameters_from_file(self.cam_path[table_number - 1])
            world_to_camera = Transform.from_matrix(np.load(self.world_calibration_path[table_number - 1]))

            return TableCameraConfiguration(table_number, cam_param, world_to_camera)
        else:
            raise ValueError("Invalid table number.")
