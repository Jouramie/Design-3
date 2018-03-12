import cv2
import copy
import numpy as np
from .vision_exception import VisionException
from src.domain.environment.environment import *

obstacle_file = '../fig/2018-02-10/obstacles10.jpg'

THICKNESS = 2


class WorldVision:
    def __init__(self):
        pass

    def create_environment(self, image_location):
        cropped_image = self.__crop_environment(image_location)
        cropped_image_copy = copy.copy(cropped_image)

        cubes = []
        obstacles = []

        for cube in self.__find_color_cubes(cropped_image, Color.BLUE):
            cubes.append(cube)
            self.__draw_cube(cropped_image_copy, cube)

        for cube in self.__find_color_cubes(cropped_image, Color.GREEN):
            cubes.append(cube)
            self.__draw_cube(cropped_image_copy, cube)

        for cube in self.__find_color_cubes(cropped_image, Color.RED):
            cubes.append(cube)
            self.__draw_cube(cropped_image_copy, cube)

        for cube in self.__find_color_cubes(cropped_image, Color.YELLOW):
            cubes.append(cube)
            self.__draw_cube(cropped_image_copy, cube)

        for cube in self.__find_black_cubes(cropped_image):
            cubes.append(cube)
            self.__draw_cube(cropped_image_copy, cube)

        for cube in self.__find_white_cube(cropped_image):
            cubes.append(cube)
            self.__draw_cube(cropped_image_copy, cube)

        target_zone = self.__find_target_zone(cropped_image)
        self.__draw_target_zone(cropped_image_copy, target_zone)

        for obstacle in self.__find_obstacles(cropped_image):
            obstacles.append(obstacle)
            self.__draw_obstacle(cropped_image_copy, obstacle)

        return Environment(cubes, obstacles, target_zone), cropped_image_copy

    def __draw_cube(self, image, cube: Cube):
        cv2.rectangle(image, cube.get_corner(0), cube.get_corner(1), cube.color.bgr, thickness=THICKNESS)

    def __draw_target_zone(self, image, target_zone: TargetZone):
        cv2.rectangle(image, target_zone.corners[0], target_zone.corners[1], Color.SKY_BLUE.bgr, thickness=THICKNESS)

    def __draw_obstacle(self, image, obstacle: Obstacle):
        cv2.circle(image, obstacle.center, obstacle.radius, Color.PINK.bgr, thickness=THICKNESS, lineType=cv2.LINE_AA)

    def __find_color_cubes(self, original_image, color: Color):
        image = cv2.medianBlur(original_image, 5)
        image = cv2.GaussianBlur(image, (5, 5), 0)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, color.lower_bound, color.upper_bound)

        image_with_contours, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            if 200 > cv2.arcLength(contour, True) > 50 and (
                    (contour[0][0][0] > 480 and contour[0][0][1] > 245) or (
                    contour[0][0][0] > 460 and contour[0][0][1] < 45) or
                    contour[0][0][0] > 570):
                yield self.__create_cube(contour, color)

    def __find_black_cubes(self, original_image):
        image = cv2.medianBlur(original_image, 5)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        kernel = np.ones((5, 5), np.uint8)

        image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.erode(image, kernel, iterations=1)

        _, thresh = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)
        image_with_contours, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if 150 > cv2.arcLength(contour, True) > 60 and (
                    (contour[0][0][0] > 470 and contour[0][0][1] > 245) or (
                    contour[0][0][0] > 470 and contour[0][0][1] < 45) or
                    contour[0][0][0] > 570):
                yield self.__create_cube(contour, Color.BLACK)

    def __find_white_cube(self, original_image) -> [Cube]:
        image = cv2.medianBlur(original_image, 5)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, Color.WHITE.lower_bound, Color.WHITE.upper_bound)

        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        cv2.imshow('white', img)

        for contour in contours:
            if 200 > cv2.arcLength(contour, True) > 1 and ((contour[0][0][0] > 480 and contour[0][0][1] > 245) or
                                                (460 < contour[0][0][0] < 610 and contour[0][0][1] < 45) or (contour[0][0][1] > 500)):
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
            if cv2.arcLength(shape, True) > 300 and shape[0][0][0] > 50:
                return self.__create_target_zone(shape)

    def __create_target_zone(self, contour) -> TargetZone:
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w / 2, y + h / 2)
        corners = [(x, y), (x + w, y + h)]
        return TargetZone(center, corners)

    def __find_obstacles(self, original_image) -> [Obstacle]:
        im = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        im = cv2.GaussianBlur(im, (5, 5), 0)

        contours = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=20, maxRadius=40)

        if contours is not None:
            for contour in contours[0]:
                yield self.__create_obstacle(contour)

    def __create_obstacle(self, contour) -> Obstacle:
        center = (contour[0], contour[1])
        radius = contour[2]
        return Obstacle(center, radius)

    def __crop_environment(self, filename):
        original_image = cv2.imread(filename)

        image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)
        image_with_contours, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        y_adjustment = 5

        crop_img = None

        for contour in contours:
            if cv2.arcLength(contour, True) > 1500:
                x, y, w, h = cv2.boundingRect(contour)
                crop_img = original_image[y + y_adjustment:y + h, x:x + w + 3]

        if crop_img is None:
            raise VisionException('Impossible to crop image.')

        return crop_img
