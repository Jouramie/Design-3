from src.domain.environments.real_world_environment import RealWorldEnvironment
from src.domain.environments.vision_environment import VisionEnvironment
from src.domain.objects.target_zone import TargetZone
from src.vision.coordinate_converter import CoordinateConverter


class RealWorldEnvironmentFactory(object):
    def __init__(self, coordinate_converter: CoordinateConverter):
        self.coordinate_converter = coordinate_converter

    def create_real_world_environment(self, vision_environment: VisionEnvironment) -> RealWorldEnvironment:
        obstacles = self.coordinate_converter.project_obstacles_from_pixel_to_real_world(vision_environment.obstacles)
        cubes = self.coordinate_converter.convert_vision_cubes_to_real_world_environment_cubes(vision_environment.cubes)
        target_zone = TargetZone(None, None)  # TODO

        return RealWorldEnvironment(obstacles, cubes, target_zone)
