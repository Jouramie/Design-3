import cv2
import copy
from vision.hsv_enum import *
from vision.bgr_enum import *
from src.domain.environment.cube import *
from src.domain.environment.environment import *

cube_file = '../fig/2018-02-25/17h43.jpg'
obstacle_file = '../fig/2018-02-10/obstacles10.jpg'
cube_list = []


def create_environment(initial_image_file):
    initial_image_file = crop_environment(initial_image_file)
    image_file = copy.copy(initial_image_file)
    #TODO est-ce que cube_list est legit comme il est, je ne pense pas

    blue_cube_contours, centers_of_blue = find_cubes(initial_image_file, lower_blue, upper_blue)
    __draw_cubes__(image_file, blue_cube_contours, blue)

    red_cube_contours, centers_of_red = find_cubes(initial_image_file, lower_red, upper_red)
    __draw_cubes__(image_file, red_cube_contours, red)

    green_cube_contours, centers_of_green = find_cubes(initial_image_file, lower_green, upper_green)
    __draw_cubes__(image_file, green_cube_contours, green)

    yellow_cube_contours, centers_of_yellow = find_cubes(initial_image_file, lower_yellow, upper_yellow)
    __draw_cubes__(image_file, yellow_cube_contours, yellow)

    black_cube_contours, centers_of_black = find_black_cubes(initial_image_file)
    __draw_cubes__(image_file, black_cube_contours, white)

    #TODO rendre le blanc fonctionnel
    #white_cube_contours, center_of_white_cube = find_white_cube(initial_image_file)
    #draw_cube(image_file, white_cube_contours, sky_blue)

    end_area_contour, center_of_end_area = find_end_area(initial_image_file)
    image_file = draw_end_area(image_file, end_area_contour)

    centers_of_obstacles, obstacles_circles = find_obstacles(initial_image_file)
    draw_obstacles(image_file, obstacles_circles, pink)

    cv2.imshow('Cube', image_file)
    cv2.waitKey(0)

    return Environment(cube_list)


def __add_cube_to_cube_list__(centers, color):
    for center in centers:
        cube = Cube(center, color)
        cube_list.append(cube)


def __draw_cubes__(im, contours, bgr):
    for shape in contours:
        x, y, w, h = cv2.boundingRect(shape)
        cv2.rectangle(im, (x, y), (x + w, y + h), bgr, 2)

    return im


def draw_end_area(im, contours):
    for shape in contours:
        x, y, w, h = cv2.boundingRect(shape)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return im


def draw_obstacles(img, circles, bgr):
    for circle in circles:
        cv2.circle(img, (circle[0], circle[1]), circle[2], bgr, thickness=2, lineType=cv2.LINE_AA)

    return img


def find_cubes(im, lower_bound, upper_bound):
    centers_of_rect = []
    cube_contours = []

    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for shape in contours:
        if cv2.arcLength(shape, True) > 50 and shape[0][0][0] > 400:
            x, y, w, h = cv2.boundingRect(shape)
            center_of_rect = (x + w/2, y + h/2)
            centers_of_rect.append(center_of_rect)
            cube_contours.append(shape)

    __add_cube_to_cube_list__(centers_of_rect, blue)

    return cube_contours, centers_of_rect


def find_black_cubes(im):
    centers_of_rect = []
    cube_contours = []
    kernel = np.ones((5, 5), np.uint8)

    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    ret, tresh = cv2.threshold(img, 36, 255, cv2.THRESH_BINARY_INV)
    img_contours, contours, hierarchy = cv2.findContours(tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for shape in contours:
        if cv2.arcLength(shape, True) > 50 and shape[0][0][0] > 400:
            x, y, w, h = cv2.boundingRect(shape)
            center_of_rect = (x + w/2, y + h/2)
            centers_of_rect.append(center_of_rect)
            cube_contours.append(shape)

    __add_cube_to_cube_list__(centers_of_rect, black)

    return cube_contours, centers_of_rect


def find_white_cube(im):
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

    __add_cube_to_cube_list__(centers_of_rect, black)

    return cube_contours, centers_of_rect


def find_end_area(im):
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


def find_obstacles(img):
    centers_of_obstacles = []
    obstacles_circles = []

    im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    im = cv2.GaussianBlur(im, (5, 5), 0)

    circles = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=20, maxRadius=40)
    if circles is not None:
        for circle in circles[0, :]:
            centers_of_obstacles.append((circle[0], circle[1]))
            obstacles_circles.append(circle)

    return centers_of_obstacles, obstacles_circles


def crop_environment(filename):
    im = cv2.imread(filename)

    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, treshold = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
    img_contours, contours, hierarchy = cv2.findContours(treshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    for shape in contours:
        if cv2.arcLength(shape, True) > 1000:
            x, y, w, h = cv2.boundingRect(shape)
            crop_img = im[y + 5:y + h, x:x+w]

    return crop_img

create_environment(cube_file)