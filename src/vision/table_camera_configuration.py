from src.vision.camera_parameters import CameraParameters
from src.vision.transform import Transform


class TableCameraConfiguration:
    def __init__(self, id: int, cam_param: CameraParameters, world_to_camera: Transform):
        self.id = id
        self.camera_parameters = cam_param
        self.world_to_camera = world_to_camera
