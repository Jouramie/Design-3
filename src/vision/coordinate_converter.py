import cv2
import numpy as np
from scipy import spatial

from src.domain.objects.flag_cube import FlagCube
from src.domain.objects.obstacle import Obstacle
from .table_camera_configuration import TableCameraConfiguration
from .transform import Transform


class CoordinateConverter:
    def __init__(self, table_camera_config: TableCameraConfiguration, cube_dictionary: dict):
        self.world_to_camera = table_camera_config.world_to_camera
        self.camera_parameters = table_camera_config.camera_parameters
        self.table_config_cubes = cube_dictionary

    def world_from_camera(self, camera_to_object: Transform):
        return self.world_to_camera.combine(camera_to_object, True)

    def get_world_to_camera(self):
        return self.world_to_camera

    def get_camera_to_world(self):
        return self.world_to_camera.inverse()

    def project_obstacles_from_pixel_to_real_world(self, obstacles: [Obstacle]) -> [Obstacle]:
        return list(map(self.project_obstacle_from_pixel_to_real_world, obstacles))

    def project_obstacle_from_pixel_to_real_world(self, obstacle: Obstacle) -> Obstacle:
        object_points = np.array([(0, 0, 41), (6.3, 0, 41), (-6.3, 0, 41), (0, 6.3, 41), (0, -6.3, 41)], 'float32')

        image_points = np.array([obstacle.center,
                                 (obstacle.center[0] + obstacle.radius, obstacle.center[1]),
                                 (obstacle.center[0] - obstacle.radius, obstacle.center[1]),
                                 (obstacle.center[0], obstacle.center[1] + obstacle.radius),
                                 (obstacle.center[0], obstacle.center[1] - obstacle.radius)])

        _, rotation_vector, translation_vector = cv2.solvePnP(object_points, image_points,
                                                              self.camera_parameters.camera_matrix,
                                                              self.camera_parameters.distortion)

        camera_to_obstacle = Transform.from_parameters(np.asscalar(translation_vector[0]),
                                                       np.asscalar(translation_vector[1]),
                                                       np.asscalar(translation_vector[2]),
                                                       np.asscalar(rotation_vector[0]),
                                                       np.asscalar(rotation_vector[1]),
                                                       np.asscalar(rotation_vector[2]))

        world_to_obstacle = self.world_from_camera(camera_to_obstacle)

        obstacle_information = world_to_obstacle.to_parameters(True)
        return Obstacle((obstacle_information[0], obstacle_information[1]), 7)

    def project_points_from_real_world_to_pixel(self, points):
        camera_to_world_parameters = self.get_camera_to_world().to_parameters()
        camera_to_world_tvec = np.array(
            [camera_to_world_parameters[0], camera_to_world_parameters[1], camera_to_world_parameters[2]])
        camera_to_world_rvec = np.array(
            [camera_to_world_parameters[3], camera_to_world_parameters[4], camera_to_world_parameters[5]])
        projected_points, _ = cv2.projectPoints(points, camera_to_world_rvec, camera_to_world_tvec,
                                                self.camera_parameters.camera_matrix, self.camera_parameters.distortion)

        return projected_points

    def convert_vision_cubes_to_real_world_environment_cubes(self, vision_cubes) -> [FlagCube]:
        real_cubes = []
        cube_pixel_positions_x_list = []
        cube_pixel_positions_y_list = []
        for table_cube in self.table_config_cubes.values():
            pixel_x = table_cube['pixel_x']
            pixel_y = table_cube['pixel_y']
            cube_pixel_positions_x_list.append(pixel_x)
            cube_pixel_positions_y_list.append(pixel_y)
        pixel_x_nparray = np.asarray(cube_pixel_positions_x_list)
        pixel_y_nparray = np.asarray(cube_pixel_positions_y_list)
        combined_x_y_arrays = np.dstack([pixel_x_nparray.ravel(), pixel_y_nparray.ravel()])[0]
        tree = spatial.cKDTree(combined_x_y_arrays)
        for vision_cube in vision_cubes:
            dist, indexes = tree.query(vision_cube.get_center())
            table_cube = self.table_config_cubes['cube' + str(indexes)]
            position = (table_cube['x'], table_cube['y'])
            color = vision_cube.get_color()
            flag_cube = FlagCube(position, color)
            real_cubes.append(flag_cube)

        return real_cubes
