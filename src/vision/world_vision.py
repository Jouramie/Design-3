import copy

import cv2
import numpy as np

from src.domain.color import Color
from src.domain.vision_environment.cube import Cube
from src.domain.vision_environment.environment import Environment
from src.domain.vision_environment.obstacle import Obstacle
from src.domain.vision_environment.target_zone import TargetZone
from .vision_exception import VisionException

from logging import Logger

obstacle_file = '../fig/2018-02-10/obstacles10.jpg'

THICKNESS = 2


class WorldVision:
    def __init__(self, logger: Logger, config: dict):
        self.logger = logger
        self.config = config

    def create_environment(self, frame):
        cropped_image = self.__crop_environment(frame)
        # cropped_image_copy = copy.copy(cropped_image)

        cubes = []
        obstacles = []

        for cube in self.__find_color_cubes(cropped_image, Color.BLUE):
            cubes.append(cube)

        for cube in self.__find_color_cubes(cropped_image, Color.GREEN):
            cubes.append(cube)

        for cube in self.__find_color_cubes(cropped_image, Color.RED):
            cubes.append(cube)

        for cube in self.__find_color_cubes(cropped_image, Color.YELLOW):
            cubes.append(cube)

        for cube in self.__find_black_cubes(cropped_image):
            cubes.append(cube)

        for cube in self.__find_white_cube(cropped_image):
            cubes.append(cube)

        target_zone = self.__find_target_zone(cropped_image)

        for obstacle in self.__find_obstacles(cropped_image):
            obstacles.append(obstacle)

        for cube in cubes:
            cube.center = (cube.center[0], cube.center[1] + 210)
            new_corners = []
            for corner in cube.corners:
                new_corners.append((corner[0], corner[1] + 210))
            cube.corners = new_corners

        if target_zone is not None:
            target_zone.center = (target_zone.center[0], target_zone.center[1] + 210)
            new_corners = []
            for corner in target_zone.corners:
                new_corners.append((corner[0], corner[1] + 210))
            target_zone.corners = new_corners

        for obstacle in obstacles:
            obstacle.center = (int(obstacle.center[0]), int(obstacle.center[1] + 210))
            print(str(obstacle.center))
            print(str(obstacle.radius))

        return Environment(cubes, obstacles, target_zone)

    def __find_color_cubes(self, original_image, color: Color):
        image = cv2.medianBlur(original_image, 5)
        image = cv2.GaussianBlur(image, (5, 5), 0)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, color.lower_bound, color.upper_bound)

        image_with_contours, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 400 > cv2.arcLength(contour, True) > 200:
                if ((1481 > x > 1115) and (313 > y > 158)) or (1481 < x and (158 < y < 1053)) or (
                        (1115 < x < 1481) and (890 < y < 1053)):
                    yield self.__create_cube(contour, color)

    def __find_black_cubes(self, frame):
        #cropped_frame = self.__crop_environment(frame)
        #frame_copy = cropped_frame[0]
        #h = cropped_frame[1]
        #w = cropped_frame[2]
        kernel = np.ones((5, 5), np.uint8)

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)
        image_with_contours, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 400 > cv2.arcLength(contour, True) > 200:
                if ((1481 > x > 1115) and (313 > y > 158)) or (1481 < x and (158 < y < 1053)) or (
                        (1115 < x < 1481) and (890 < y < 1053)):
                    #contour[0][0][1] += h
                    #contour[0][0][1] += w
                    yield self.__create_cube(contour, Color.BLACK)

    def __find_white_cube(self, original_image) -> [Cube]:
        image = cv2.medianBlur(original_image, 5)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, Color.WHITE.lower_bound, Color.WHITE.upper_bound)

        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 400 > cv2.arcLength(contour, True) > 100:
                if ((1481 > x > 1115) and (313 > y > 158)) or (1481 < x and (158 < y < 1053)) or (
                        (1115 < x < 1481) and (890 < y < 1053)):
                    yield self.__create_cube(contour, Color.WHITE)

    def __create_cube(self, contour, color: Color) -> Cube:
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w / 2, y + h / 2)
        return Cube(center, color, [(x, y), (x + w, y + h)])

    def __find_target_zone(self, original_image) -> TargetZone:
        hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_image, Color.TARGET_ZONE_GREEN.lower_bound, Color.TARGET_ZONE_GREEN.upper_bound)

        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for shape in contours:
            x = shape[0][0][0]
            if cv2.arcLength(shape, True) > 2000 and x > 50:
                return self.__create_target_zone(shape)

    def __create_target_zone(self, contour) -> TargetZone:
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w / 2, y + h / 2)
        corners = [(x, y), (x + w, y + h)]
        return TargetZone(center, corners)

    def __find_obstacles(self, original_image) -> [Obstacle]:
        im = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        im = cv2.GaussianBlur(im, (5, 5), 0)

        contours = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=50, maxRadius=80)

        if contours is not None:
            for contour in contours[0]:
                yield self.__create_obstacle(contour)

    def __create_obstacle(self, contour) -> Obstacle:
        center = (contour[0], contour[1])
        radius = contour[2]
        return Obstacle(center, radius)

    def __crop_environment(self, frame):
        x, y, w, h = (0, 200, 1600, 800)
        crop_img = frame[y:y + h, x:x + w]

        #cv2.imshow('dsaf', crop_img)
        #cv2.waitKey(0)

        return crop_img
