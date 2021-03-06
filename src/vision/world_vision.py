import os
import time
from logging import Logger

import cv2

from src.domain.environments.vision_environment import VisionEnvironment
from src.domain.objects.color import Color
from src.domain.objects.obstacle import Obstacle
from src.domain.objects.vision_cube import VisionCube
from src.vision.table_crop import TableCrop


class WorldVision:
    def __init__(self, logger: Logger, config: dict):
        self.logger = logger
        self.config = config

    def create_environment(self, frame, table):
        self.__log_frame(frame)

        options = {1: TableCrop.TABLE1, 2: TableCrop.TABLE2, 3: TableCrop.TABLE3, 4: TableCrop.TABLE4,
                   5: TableCrop.TABLE5, 6: TableCrop.TABLE6}
        table_crop = options[table]
        cropped_image = self.__crop_environment(frame, table_crop)

        cubes = []
        obstacles = []

        cubes = self.__validate_red_cube_is_present(cropped_image, cubes)
        cubes = self.__validate_cube_is_present(cropped_image, Color.BLUE, cubes)
        cubes = self.__validate_cube_is_present(cropped_image, Color.GREEN, cubes)
        cubes = self.__validate_cube_is_present(cropped_image, Color.YELLOW, cubes)
        cubes = self.__validate_white_cube_is_present(cropped_image, cubes)
        cubes = self.__validate_cube_is_present(cropped_image, Color.BLACK, cubes)

        for obstacle in self.__find_obstacles(cropped_image):
            obstacles.append(obstacle)

        for cube in cubes:
            cube.center = (cube.center[0], cube.center[1] + table_crop.y_crop_top)
            new_corners = []
            for corner in cube.corners:
                new_corners.append((corner[0], corner[1] + table_crop.y_crop_top))
            cube.corners = new_corners

        for obstacle in obstacles:
            obstacle.center = (int(obstacle.center[0]), int(obstacle.center[1] + table_crop.y_crop_top))

        return VisionEnvironment(cubes, obstacles)

    def __validate_cube_is_present(self, frame, color: Color, cubes):
        for cube in self.__find_color_cubes(frame, color):
            cubes.append(cube)
        return cubes

    def __validate_white_cube_is_present(self, frame, cubes):
        color = Color.WHITE
        for cube in self.__find_white_cubes(frame):
            cubes.append(cube)
        return cubes

    def __validate_red_cube_is_present(self, frame, cubes):
        for cube in self.__find_red_cubes(frame):
            cubes.append(cube)
        return cubes

    def __find_color_cubes(self, frame, color: Color):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, color.lower_bound, color.upper_bound)

        image_with_contours, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        height, width, _ = frame.shape

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 6000 > cv2.contourArea(contour) > 1000:
                if ((0.8 * width < x < 0.92 * width) and (y <= 0.10 * height) or
                        ((0.96 * width < x < width) and (0.12 * height < y <= 0.82 * height)) or
                        ((0.78 * width < x < 0.92 * width) and (0.86 * height < y < height))):
                    yield self.__create_cube(contour, color)

    def __find_white_cubes(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        color = Color.WHITE
        mask = cv2.inRange(hsv, color.lower_bound, color.upper_bound)

        image_with_contours, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        height, width, _ = frame.shape

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 5000 > cv2.contourArea(contour) > 700:
                if ((0.8 * width < x < 0.92 * width) and (y <= 0.09 * height) or
                        ((0.96 * width < x < width) and (0.10 * height < y <= 0.82 * height)) or
                        ((0.78 * width < x < 0.92 * width) and (0.86 * height < y < height))):
                    yield self.__create_cube(contour, color)

    def __find_red_cubes(self, frame):
        red = Color.RED
        red2 = Color.RED2
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        red_mask = cv2.inRange(hsv, red.lower_bound, red.upper_bound)
        red2_mask = cv2.inRange(hsv, red2.lower_bound, red2.upper_bound)

        mask = red_mask + red2_mask

        image_with_contours, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        height, width, _ = frame.shape

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 6000 > cv2.contourArea(contour) > 1000:
                if ((0.8 * width < x < 0.92 * width) and (y <= 0.8 * height) or
                        ((0.96 * width < x < width) and (0.12 * height < y <= 0.82 * height)) or
                        ((0.78 * width < x < 0.92 * width) and (0.86 * height < y < height))):
                    yield self.__create_cube(contour, Color.RED)

    def __create_cube(self, contour, color: Color) -> VisionCube:
        x, y, w, h = cv2.boundingRect(contour)
        return VisionCube(color, [(x, y), (x + w, y + h)])

    def __find_obstacles(self, frame) -> [Obstacle]:
        im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        height, width, _ = frame.shape

        im = cv2.GaussianBlur(im, (5, 5), 0)

        contours = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=50, maxRadius=60)

        if contours is not None:
            for contour in contours[0]:
                x = contour[0]
                if x > 0.4 * width:
                    yield self.__create_obstacle(contour)

    def __create_obstacle(self, contour) -> Obstacle:
        center = (contour[0], contour[1])
        radius = contour[2]
        return Obstacle(center, radius)

    def __crop_environment(self, frame, table_crop):
        x = 0
        w = 1600 - table_crop.x_crop
        y = table_crop.y_crop_top
        h = 1200 - table_crop.y_crop_top - table_crop.y_crop_bot

        crop_img = frame[y:y + h, x:x + w]

        return crop_img

    def __log_frame(self, frame):
        directory = self.config['camera']['image_save_dir'].format(date=time.strftime("%Y-%m-%d"))
        if not os.path.exists(directory):
            os.makedirs(directory)
        cv2.imwrite(directory + time.strftime("/%Hh%Mm%Ss.jpg"), frame)
