import cv2
import numpy as np

from src.domain.environments.vision_environment import VisionEnvironment
from src.domain.objects.obstacle import Obstacle
from src.vision.coordinate_converter import CoordinateConverter
from src.vision.table_camera_configuration import TableCameraConfiguration
from src.vision.transform import Transform


class RealWorldEnvironment(object):
    def __init__(self, vision_environment: VisionEnvironment, table_camera_config: TableCameraConfiguration,
                 coordinate_converter: CoordinateConverter):
        self.__table_camera_config = table_camera_config
        self.__coordinate_converter = coordinate_converter
        # TODO déplacer dans une factory
        self.obstacles = self.__project_obstacles(vision_environment.obstacles)

    def __project_obstacles(self, obstacles: [Obstacle]) -> [Obstacle]:
        return list(map(self.__project_obstacle, obstacles))

    def __project_obstacle(self, obstacle: Obstacle) -> Obstacle:
        object_points = np.array([(0, 0, 41), (6.3, 0, 41), (-6.3, 0, 41), (0, 6.3, 41), (0, -6.3, 41)], 'float32')

        image_points = np.array([obstacle.center,
                                 (obstacle.center[0] + obstacle.radius, obstacle.center[1]),
                                 (obstacle.center[0] - obstacle.radius, obstacle.center[1]),
                                 (obstacle.center[0], obstacle.center[1] + obstacle.radius),
                                 (obstacle.center[0], obstacle.center[1] - obstacle.radius)])

        _, rotation_vector, translation_vector = cv2.solvePnP(object_points, image_points,
                                                              self.__table_camera_config.cam_param.camera_matrix,
                                                              self.__table_camera_config.cam_param.distortion)

        camera_to_obstacle = Transform.from_parameters(np.asscalar(translation_vector[0]),
                                                       np.asscalar(translation_vector[1]),
                                                       np.asscalar(translation_vector[2]),
                                                       np.asscalar(rotation_vector[0]),
                                                       np.asscalar(rotation_vector[1]),
                                                       np.asscalar(rotation_vector[2]))

        world_to_obstacle = self.__coordinate_converter.world_from_camera(camera_to_obstacle)

        obstacle_information = world_to_obstacle.to_parameters(True)
        return Obstacle((obstacle_information[0], obstacle_information[1]), 6.3)
