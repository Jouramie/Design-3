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

        robot_projected_points = self.coordinate_converter.project_points(robot_corners)

        cv2.line(frame, tuple(robot_projected_points[0][0]), tuple(robot_projected_points[1][0]), (204, 0, 204), 3)
        cv2.line(frame, tuple(robot_projected_points[1][0]), tuple(robot_projected_points[2][0]), (204, 0, 204), 3)
        cv2.line(frame, tuple(robot_projected_points[2][0]), tuple(robot_projected_points[3][0]), (204, 0, 204), 3)
        cv2.line(frame, tuple(robot_projected_points[3][0]), tuple(robot_projected_points[0][0]), (204, 0, 204), 3)

        self.__draw_robot_radius(frame, robot_projected_points)

    def draw_real_path(self, frame, points):
        i = 0
        if len(points) != 0:
            world_points = self.coordinate_converter.project_points(points)
            number_of_points = (len(world_points) - 1)
            while i < number_of_points:
                cv2.line(frame, tuple(world_points[i][0]), tuple(world_points[i + 1][0]), Color.LIGHT_BLUE.bgr, 3)
                i = i + 1

    def draw_planned_path(self, frame, points):
        for point in points:
            np_points = np.array([(point[0][0], point[0][1], 0), (point[1][0], point[1][1], 0)], 'float32')
            projected_points = self.coordinate_converter.project_points(np_points)

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

    def __draw_target_zone(self, frame, target_zone: TargetZone) -> None:
        if target_zone is None:
            self.logger.warning("Target zone is None.")
        else:
            cv2.rectangle(frame, target_zone.corners[0], target_zone.corners[1], Color.SKY_BLUE.bgr, thickness=3)

    def __draw_obstacle(self, frame, obstacle: Obstacle) -> None:
        cv2.circle(frame, (int(obstacle.center[0]), int(obstacle.center[1])), int(obstacle.radius), Color.PINK.bgr,
                   thickness=3, lineType=cv2.LINE_AA)

    def draw_real_world_environment(self, frame, real_world_environment: RealWorldEnvironment):
        for obstacle in real_world_environment.obstacles:
            self.__project_and_draw_real_obstacle(frame, obstacle)
        for cube in real_world_environment.cubes:
            self.__project_and_draw_real_cube(frame, cube)

    def __project_and_draw_real_obstacle(self, frame, obstacle: Obstacle) -> None:
        real_positions = np.array([(obstacle.center[0], obstacle.center[1], 0.0),
                                   (obstacle.center[0] + obstacle.radius, obstacle.center[1], 0.0)], 'float32')
        image_positions = self.coordinate_converter.project_points(real_positions)

        cv2.circle(frame, tuple(image_positions[0][0]), image_positions[1][0][0] - image_positions[0][0][0],
                   Color.PINK2.bgr,
                   thickness=3, lineType=cv2.LINE_AA)

    def __project_and_draw_real_cube(self, frame, flag_cube: FlagCube) -> None:
        cube_centers = flag_cube.get_3d_corners()
        real_positions = np.array(cube_centers, 'float32')
        image_positions = self.coordinate_converter.project_points(real_positions)

        cv2.rectangle(frame, tuple(image_positions[0][0]), tuple(image_positions[1][0]), flag_cube.color.bgr,
                      thickness=3)
