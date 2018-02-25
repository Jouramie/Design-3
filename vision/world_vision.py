import cv2
import copy
from vision.hsv_enum import *
from vision.bgr_enum import *

cube_file = '../fig/2018-02-10/16h42.png';
obstacle_file = '../fig/2018-02-10/obstacles10.jpg';


def create_environment(initial_image_file):
    initial_image_file = crop_environment(initial_image_file)
    image_file = copy.copy(initial_image_file)

    blue_cube_contours, center_of_blue_rect = find_cube(initial_image_file, lower_blue, upper_blue)
    image_file = draw_cube(image_file, blue_cube_contours, blue)

    red_cube_contours, center_of_red_rect = find_cube(initial_image_file, lower_red, upper_red)
    image_file = draw_cube(image_file, red_cube_contours, red)

    green_cube_contours, center_of_green_rect = find_cube(initial_image_file, lower_green, upper_green)
    image_file = draw_cube(image_file, green_cube_contours, green)

    yellow_cube_contours, center_of_yellow_rect = find_cube(initial_image_file, lower_yellow, upper_yellow)
    image_file = draw_cube(image_file, yellow_cube_contours, yellow)

    black_cube_contours, center_of_black_rect = find_black_cube(initial_image_file)
    image_file = draw_cube(image_file, black_cube_contours, white)

    white_cube_contours, center_of_white_cube = find_white_cube(initial_image_file)
    image_file = draw_cube(image_file, white_cube_contours, sky_blue)

    #end_area_contours, center_of_end_area = find_end_area(initial_image_file)
    #image_file = draw_end_area(image_file, end_area_contours)

    obstacle_test = crop_environment(obstacle_file)
    centers_of_obstacles, obstacles_circles = find_obstacles(obstacle_test)
    obstacle_test = draw_obstacles(obstacle_test, obstacles_circles, sky_blue)

    cv2.imshow('Cube', image_file)
    cv2.waitKey(0)

    cv2.imshow('Obstacles', obstacle_test)
    cv2.waitKey(0)

    #return center_of_blue_rect, center_of_red_rect, center_of_green_rect, center_of_yellow_rect, center_of_black_rect


def draw_cube(im, contours, bgr):
    for shape in contours:
        x, y, w, h = cv2.boundingRect(shape)
        cv2.rectangle(im, (x, y), (x + w, y + h), bgr, 2)

    return im


def draw_end_area(im, contours):
    for shape in contours:
        if 800 > len(shape) > 600 and shape[0][0][0] > 50:
            x, y, w, h = cv2.boundingRect(shape)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return im


def draw_obstacles(img, circles, bgr):
    for circle in circles:
        cv2.circle(img, (circle[0], circle[1]), circle[2], bgr, thickness=2, lineType=cv2.LINE_AA)

    return img


def find_cube(im, lower_bound, upper_bound):
    center_of_rect = ''
    cube_contours = []

    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE);

    for shape in contours:
        if cv2.arcLength(shape, True) > 50 and shape[0][0][0] > 400:
            x, y, w, h = cv2.boundingRect(shape)
            center_of_rect = (x + w/2, y + h/2)
            cube_contours.append(shape)

    return cube_contours, center_of_rect


def find_black_cube(im):
    center_of_rect = ''
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
            cube_contours.append(shape)

    return cube_contours, center_of_rect


def find_white_cube(im):
    center_of_rect = ''
    cube_contours = []
    kernel = np.ones((5, 5), np.uint8)

    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    img = cv2.erode(img, kernel, iterations=1)
    img = cv2.dilate(img, kernel, iterations=1)

    ret, tresh = cv2.threshold(img, 36, 255, cv2.THRESH_BINARY)
    img_contours, contours, hierarchy = cv2.findContours(tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for shape in contours:
        if cv2.arcLength(shape, True) > 50 and shape[0][0][0] > 400 and shape[0][0][1] < 296:
            x, y, w, h = cv2.boundingRect(shape)
            center_of_rect = (x + w/2, y + h/2)
            cube_contours.append(shape)

    return cube_contours, center_of_rect


def find_end_area(im):
    center_of_end_area = ''

    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_green, upper_green)

    img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE);

    for shape in contours:
        if 800 > len(shape) > 600 and shape[0][0][0] > 50:
            x, y, w, h = cv2.boundingRect(shape)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center_of_end_area = (x + w/2, y + h/2)

    return contours, center_of_end_area


def find_obstacles(img):
    centers_of_obstacles = []
    obstacles_circles = []

    im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    im = cv2.GaussianBlur(im, (5, 5), 0)

    circles = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=20, maxRadius=40)
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
        if len(shape) > 400:
            x, y, w, h = cv2.boundingRect(shape)
            crop_img = im[y:y + h, x:x + w]

    return crop_img


create_environment(cube_file)
