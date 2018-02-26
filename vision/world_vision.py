import cv2
import copy
from vision.hsv_enum import *
from vision.bgr_enum import *
from src.domain.environment.environment import *

obstacle_file = '../fig/2018-02-10/obstacles10.jpg'


class WorldVision:
    def __init__(self):
        self.cube_list = []
        self.obstacle_list = []

    def create_environment(self, initial_image_file):
        initial_image_file = self.__crop_environment__(initial_image_file)
        image_file = copy.copy(initial_image_file)

        blue_cube_contours, centers_of_blue = self.__find_cubes__(initial_image_file, lower_blue, upper_blue, blue)
        self.__draw_cubes__(image_file, blue_cube_contours, blue)

        red_cube_contours, centers_of_red = self.__find_cubes__(initial_image_file, lower_red, upper_red, red)
        self.__draw_cubes__(image_file, red_cube_contours, red)

        green_cube_contours, centers_of_green = self.__find_cubes__( initial_image_file, lower_green, upper_green, green)
        self.__draw_cubes__(image_file, green_cube_contours, green)

        yellow_cube_contours, centers_of_yellow = self.__find_cubes__(initial_image_file, lower_yellow, upper_yellow, yellow)
        self.__draw_cubes__(image_file, yellow_cube_contours, yellow)

        black_cube_contours, centers_of_black = self.__find_black_cubes__(initial_image_file)
        self.__draw_cubes__(image_file, black_cube_contours, white)

        #TODO rendre le blanc fonctionnel
        #white_cube_contours, center_of_white_cube = find_white_cube(initial_image_file)
        #draw_cube(image_file, white_cube_contours, sky_blue)

        end_area_contour, center_of_end_area = self.__find_end_area__(initial_image_file)
        self.__draw_end_area__(image_file, end_area_contour)

        centers_of_obstacles, obstacles_circles = self.__find_obstacles__(initial_image_file)
        self.__draw_obstacles__(image_file, obstacles_circles, pink)

        return Environment(self.cube_list, self.obstacle_list, center_of_end_area), image_file

    def __draw_cubes__(self, im, contours, bgr):
        for shape in contours:
            x, y, w, h = cv2.boundingRect(shape)
            cv2.rectangle(im, (x, y), (x + w, y + h), bgr, 2)

        return im

    def __draw_end_area__(self, im, contours):
        for shape in contours:
            x, y, w, h = cv2.boundingRect(shape)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return im

    def __draw_obstacles__(self, img, circles, bgr):
        for circle in circles:
            cv2.circle(img, (circle[0], circle[1]), circle[2], bgr, thickness=2, lineType=cv2.LINE_AA)

        return img

    def __find_cubes__(self, im, lower_bound, upper_bound, color):
        centers_of_rect = []
        cube_contours = []

        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for shape in contours:
            if 200 > cv2.arcLength(shape, True) > 50 and shape[0][0][0] > 400:
                x, y, w, h = cv2.boundingRect(shape)
                center_of_rect = (x + w/2, y + h/2)
                centers_of_rect.append(center_of_rect)
                cube_contours.append(shape)

        self.__add_cube_to_cube_list__( centers_of_rect, color)

        return cube_contours, centers_of_rect

    def __add_cube_to_cube_list__(self, centers, color):
        for center in centers:
            cube = Cube(center, color)
            self.cube_list.append(cube)

    def __find_black_cubes__(self, im):
        centers_of_rect = []
        cube_contours = []
        kernel = np.ones((5, 5), np.uint8)

        img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        ret, tresh = cv2.threshold(img, 36, 255, cv2.THRESH_BINARY_INV)
        img_contours, contours, hierarchy = cv2.findContours(tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for shape in contours:
            if 150 > cv2.arcLength(shape, True) > 60 and ((shape[0][0][0] > 480 and shape[0][0][1] > 245) or (shape[0][0][0] > 480 and shape[0][0][1] < 45) or shape[0][0][0] > 570):
                x, y, w, h = cv2.boundingRect(shape)
                center_of_rect = (x + w/2, y + h/2)
                centers_of_rect.append(center_of_rect)
                cube_contours.append(shape)

        self.__add_cube_to_cube_list__(centers_of_rect, black)

        return cube_contours, centers_of_rect

    def __find_white_cube__(self, im):
        centers_of_rect = []
        cube_contours = []
        kernel = np.ones((5, 5), np.uint8)

        '''
        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_white, lower_white)

        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        cv2.imshow('white', img)
        '''

        img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.dilate(img, kernel, iterations=1)

        ret, tresh = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY_INV)
        img_contours, contours, hierarchy = cv2.findContours(tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow('white', img_contours)
        cv2.waitKey(0)

        for shape in contours:
            if cv2.arcLength(shape, True) > 20 and shape[0][0][0] > 500 and shape[0][0][1] < 296:
                x, y, w, h = cv2.boundingRect(shape)
                centers_of_rect.append(x + w/2, y + h/2)
                cube_contours.append(shape)

        self.__add_cube_to_cube_list__(centers_of_rect, black)

        return cube_contours, centers_of_rect

    def __find_end_area__(self, im):
        center_of_end_area = ''
        end_area_contour = ''

        hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_green, upper_green)

        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for shape in contours:
            if cv2.arcLength(shape, True) > 300 and shape[0][0][0] > 50:
                end_area_contour = shape
                x, y, w, h = cv2.boundingRect(shape)
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                center_of_end_area = (x + w/2, y + h/2)

        return end_area_contour, center_of_end_area

    def __find_obstacles__(self, img):
        centers_of_obstacles = []
        obstacles_circles = []

        im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        im = cv2.GaussianBlur(im, (5, 5), 0)

        circles = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=20, maxRadius=40)
        if circles is not None:
            for circle in circles[0, :]:
                centers_of_obstacles.append((circle[0], circle[1]))
                obstacles_circles.append(circle)
            self.__add_obstacle_to_obstacle_list__(circles)

        return centers_of_obstacles, obstacles_circles

    def __add_obstacle_to_obstacle_list__(self, circles):
        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            obstacle = Obstacle(center)
            self.obstacle_list.append(obstacle)

    def __crop_environment__(self, filename):
        im = cv2.imread(filename)

        img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        ret, treshold = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
        img_contours, contours, hierarchy = cv2.findContours(treshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        img = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

        y_adjustment = 5

        for shape in contours:
            if cv2.arcLength(shape, True) > 1000:
                x, y, w, h = cv2.boundingRect(shape)
                crop_img = im[y + y_adjustment:y + h, x:x+w]

        return crop_img

