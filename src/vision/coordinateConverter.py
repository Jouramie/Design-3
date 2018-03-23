from src.vision.transform import Transform


class CoordinateConverter:
    def __init__(self, world_to_camera: Transform):
        self.world_to_camera = world_to_camera

    def world_from_camera(self, camera_to_object: Transform):
        return self.world_to_camera.combine(camera_to_object, True)

    def get_world_to_camera(self):
        return self.world_to_camera

    def get_camera_to_world(self):
        return self.world_to_camera.inverse()
