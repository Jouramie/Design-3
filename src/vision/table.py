from src.vision.transform import Transform
from src.vision.cameraParameters import CameraParameters


class Table:
    def __init__(self, id: int, cam_param: CameraParameters, world_to_camera: Transform):
        self.id = id
        self.camParam = cam_param
        self.world_to_camera = world_to_camera
