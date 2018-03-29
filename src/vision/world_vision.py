import copy

import cv2
import numpy as np

from src.domain.color import Color
from src.domain.vision_environment.cube import Cube
from src.domain.vision_environment.environment import Environment
from src.domain.vision_environment.obstacle import Obstacle
from src.domain.vision_environment.target_zone import TargetZone
from .vision_exception import VisionException

obstacle_file = '../fig/2018-02-10/obstacles10.jpg'

THICKNESS = 2


class WorldVision:
    def __init__(self):
        pass

    def create_environment(self, frame):
        #cropped_image = self.__crop_environment(image_location)
        #cropped_image_copy = copy.copy(cropped_image)

        cubes = []
        obstacles = []

        cv2.imshow("frame", frame)
        cv2.waitKey(0)

        for cube in self.__find_color_cubes(frame, Color.BLUE):
            cubes.append(cube)

        for cube in self.__find_color_cubes(frame, Color.GREEN):
            cubes.append(cube)

        for cube in self.__find_color_cubes(frame, Color.RED):
            cubes.append(cube)

        for cube in self.__find_color_cubes(frame, Color.YELLOW):
            cubes.append(cube)

        for cube in self.__find_black_cubes(frame):
            cubes.append(cube)

        for cube in self.__find_white_cube(frame):
            cubes.append(cube)

        target_zone = self.__find_target_zone(frame)

        for obstacle in self.__find_obstacles(frame):
            obstacles.append(obstacle)

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
                if ((1481 > x > 1115) and (313 > y > 158)) or (1481 < x  and (158 < y < 1053)) or ((1115 < x < 1481) and (890 < y < 1053)):
                    yield self.__create_cube(contour, color)

    def __find_black_cubes(self, frame):

        frame_copy = self.__crop_environment(frame)[0]
        frame_copy = cv2.medianBlur(frame_copy, 5)
        frame_copy = cv2.GaussianBlur(frame_copy, (5, 5), 0)
        kernel = np.ones((5, 5), np.uint8)

        image = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.erode(image, kernel, iterations=1)

        h = self.__crop_environment(frame)[1]
        w = self.__crop_environment(frame)[2]

        #cv2.imshow('frame', image)

        _, thresh = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)
        image_with_contours, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 400 > cv2.arcLength(contour, True) > 200:
                if ((1481 > x > 1115) and (313 > y > 158)) or (1481 < x and (158 < y < 1053)) or ((1115 < x < 1481) and (890 < y < 1053)):
                    contour[0][0][1] += h
                    contour[0][0][1] += w
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
                if ((1481 > x > 1115) and (313 > y > 158)) or (1481 < x  and (158 < y < 1053)) or ((1115 < x < 1481) and (890 < y < 1053)):
                    yield self.__create_cube(contour, Color.WHITE)

    def __create_cube(self, contour, color: Color) -> Cube:
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w / 2, y + h / 2)
        return Cube(center, color, [(x, y), (x + w, y + h)])

    def __find_target_zone(self, original_image) -> TargetZone:
        hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_image, Color.GREEN.lower_bound, Color.GREEN.upper_bound)

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

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)
        image_with_contours, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        crop_img = None

        for contour in contours:
            if cv2.arcLength(contour, True) > 5000:
                x, y, w, h = cv2.boundingRect(contour)
                crop_img = frame[y:y + h, x:x]

        if crop_img is None:
            raise VisionException('Impossible to crop image.')

        return crop_img, h, w
