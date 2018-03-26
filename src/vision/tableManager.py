import numpy as np

from src.vision.transform import Transform
from src.vision.table import Table
from src.vision.cameraParameters import CameraParameters


class TableManager:
    def __init__(self):
        self.cam_path = ["",
                         "",
                         "",
                         "../../calibration/table4_2018-03-01.yml",
                         "",
                         ""]
        self.world_calibration_path = ["",
                                       "",
                                       "",
                                       "../../calibration/world_calibration_4.npy",
                                       "",
                                       ""]

    def create_table(self, id):
        if 1 <= id <= 6:
            camParam = CameraParameters()
            camParam.readFromFile(self.cam_path[id-1])
            world_to_camera = Transform.from_matrix(np.load(self.world_calibration_path[id-1]))

            return Table(id, camParam, world_to_camera)
        else:
            raise ValueError("Invalid table number.")



