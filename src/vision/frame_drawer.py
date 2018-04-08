from logging import Logger

import cv2
import numpy as np

from src.domain.environments.real_world_environment import RealWorldEnvironment
from src.domain.environments.vision_environment import VisionEnvironment
from src.domain.objects.color import Color
from src.domain.objects.flag_cube import FlagCube
from src.domain.objects.obstacle import Obstacle
from src.domain.objects.robot import Robot
from src.domain.objects.target_zone import TargetZone
from src.domain.objects.vision_cube import VisionCube
from src.vision.coordinate_converter import CoordinateConverter


class FrameDrawer(object):
    def __init__(self, coordinate_converter: CoordinateConverter, logger: Logger):
        self.coordinate_converter = coordinate_converter
        self.logger = logger

    def draw_robot(self, frame, robot: Robot):
        robot_corners = robot.get_corners()

        robot_projected_points = self.coordinate_converter.project_points_from_real_world_to_pixel(robot_corners)

        cv2.line(frame, tuple(robot_projected_points[0][0]), tuple(robot_projected_points[1][0]), (204, 0, 204), 3)
        cv2.line(frame, tuple(robot_projected_points[1][0]), tuple(robot_projected_points[2][0]), (204, 0, 204), 3)
        cv2.line(frame, tuple(robot_projected_points[2][0]), tuple(robot_projected_points[3][0]), (204, 0, 204), 3)
        cv2.line(frame, tuple(robot_projected_points[3][0]), tuple(robot_projected_points[0][0]), (204, 0, 204), 3)

        projected_center_x = int((robot_projected_points[1][0][0] + robot_projected_points[2][0][0]) / 2)
        projected_center_y = int((robot_projected_points[1][0][1] + robot_projected_points[2][0][1]) / 2)
        robot_projected_orientation_center = (projected_center_x, projected_center_y)

        projected_center_front_x = int((robot_projected_points[0][0][0] + robot_projected_points[2][0][0]) / 2)
        projected_center_front_y = int((robot_projected_points[0][0][1] + robot_projected_points[2][0][1]) / 2)
        robot_projected_front_orientation_center = (projected_center_front_x, projected_center_front_y)

        cv2.line(frame, robot_projected_orientation_center, robot_projected_front_orientation_center, (204, 0, 204), 3)

        self.__draw_robot_radius(frame, robot_projected_points)

    def draw_real_path(self, frame, real_path):
        points = np.asarray(real_path)
        i = 0
        if len(points) != 0:
            world_points = self.coordinate_converter.project_points_from_real_world_to_pixel(points)
            number_of_points = (len(world_points) - 1)
            while i < number_of_points:
                cv2.line(frame, tuple(world_points[i][0]), tuple(world_points[i + 1][0]), Color.LIGHT_BLUE.bgr, 3)
                i = i + 1

    def draw_planned_path(self, frame, points):
        for point in points:
            np_points = np.array([(point[0][0], point[0][1], 0), (point[1][0], point[1][1], 0)], 'float32')
            projected_points = self.coordinate_converter.project_points_from_real_world_to_pixel(np_points)

            cv2.line(frame, tuple(projected_points[0][0]), tuple(projected_points[1][0]), Color.LIGHT_GREEN.bgr, 3)

    def draw_vision_environment(self, frame, vision_environment: VisionEnvironment):
        for obstacle in vision_environment.obstacles:
            self.__draw_obstacle(frame, obstacle)
        for cube in vision_environment.cubes:
            self.__draw_cube(frame, cube)

    def __draw_robot_radius(self, frame, robot_projected_points):
        size_between = (robot_projected_points[2][0] - robot_projected_points[0][0]) / 2
        center_pt = robot_projected_points[0][0] + size_between

        cv2.circle(frame, tuple(center_pt), 154, (144, 100, 40), 2, cv2.LINE_AA)

    def __draw_cube(self, frame, cube: VisionCube) -> None:
        if cube is not None:
            cv2.rectangle(frame, cube.corners[0], cube.corners[1], cube.color.bgr, thickness=3)

    def __draw_obstacle(self, frame, obstacle: Obstacle) -> None:
        if obstacle is not None:
            cv2.circle(frame, (int(obstacle.center[0]), int(obstacle.center[1])), int(obstacle.radius), Color.PINK.bgr,
                       thickness=3, lineType=cv2.LINE_AA)

    def draw_real_world_environment(self, frame, real_world_environment: RealWorldEnvironment):
        for obstacle in real_world_environment.obstacles:
            self.__project_and_draw_real_obstacle(frame, obstacle)
        for cube in real_world_environment.cubes:
            self.__project_and_draw_real_cube(frame, cube)
        self.__project_and_draw_target_zone(frame, real_world_environment.target_zone)

    def __project_and_draw_real_obstacle(self, frame, obstacle: Obstacle) -> None:
        radius_line = list(map(self.to_3d, obstacle.get_radius_line()))

        real_positions = np.array(radius_line, 'float32')

        image_positions = self.coordinate_converter.project_points_from_real_world_to_pixel(real_positions)

        cv2.circle(frame, tuple(image_positions[0][0]), image_positions[1][0][0] - image_positions[0][0][0],
                   Color.PINK2.bgr, thickness=3, lineType=cv2.LINE_AA)

    def __project_and_draw_real_cube(self, frame, flag_cube: FlagCube) -> None:
        cube_centers = list(map(self.to_3d, flag_cube.get_corners()))

        real_positions = np.array(cube_centers, 'float32')

        image_positions = self.coordinate_converter.project_points_from_real_world_to_pixel(real_positions)

        cv2.rectangle(frame, tuple(image_positions[0][0]), tuple(image_positions[1][0]), flag_cube.color.bgr,
                      thickness=3)

    def __project_and_draw_target_zone(self, frame, target_zone: TargetZone):
        target_zone_corners = list(map(self.to_3d, target_zone.corners))

        real_positions = np.array(target_zone_corners, 'float32')

        image_positions = self.coordinate_converter.project_points_from_real_world_to_pixel(real_positions)

        cv2.rectangle(frame, tuple(image_positions[0][0]), tuple(image_positions[1][0]), Color.TARGET_ZONE_GREEN.bgr,
                      thickness=3)

    @staticmethod
    def to_3d(point: tuple):
        return point[0], point[1], 0
