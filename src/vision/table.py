import aruco

from src.vision.transform import Transform


class Table:
    def __init__(self, id: int, cam_param: aruco.CameraParameters, world_to_camera: Transform):
        self.id = id
        self.camParam = cam_param
        self.world_to_camera = world_to_camera
