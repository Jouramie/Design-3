import cv2
from vision.hsv_enum import *

image_file = '../fig/2018-02-10/16h42.png';
obstacle_file = '../fig/2018-02-10/obstacles10.jpg';
cap = cv2.VideoCapture(0)


def create_environment():
    #image_file = crop_environment(obstacle_file)
    blue_cube = get_cube(image_file, lower_blue, upper_blue, (255, 0, 0))
    #green_cube = get_cube(image_file, lower_green, upper_green, (0, 255, 0))
    #red_cube = get_cube(image_file, lower_red, upper_red, (0, 0, 255))
    #yellow_cube = get_cube(image_file, lower_yellow, lower_yellow, (0, 0, 255))
    #end_area = get_end_area(image_file)
    #find_obstacles(obstacle_file)


def get_cube(filename, lower_bound, upper_bound, bgr):
    im = cv2.imread(filename)
    center_of_rect = ''

    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE);

    for shape in contours:
        if 200 > len(shape) > 50 and shape[0][0][0] > 400 and shape[0][0][1] > 86:
            x, y, w, h = cv2.boundingRect(shape)
            cv2.rectangle(im, (x, y), (x + w, y + h), bgr, 2)
            # TODO : Factor in the 3d objects translation to origin constant
            center_of_rect = (x + w/2, y + h/2)

    cv2.imshow('Cube', im)
    if cv2.waitKey(0):
        return center_of_rect


def get_end_area(filename):
    im = cv2.imread(filename)
    center_of_end_area = ''

    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_green, upper_green)

    img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE);

    for shape in contours:
        if 800 > len(shape) > 600 and shape[0][0][0] > 50:
            x, y, w, h = cv2.boundingRect(shape)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center_of_end_area = (x + w/2, y + h/2)

    cv2.imshow('End area', im)
    if cv2.waitKey(0):
        return center_of_end_area


def find_obstacles(filename):
    img = cv2.imread(filename)
    centers_of_obstacles = []

    im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    im = cv2.GaussianBlur(im, (5, 5), 0)

    circles = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=20, maxRadius=40)
    for circle in circles[0, :]:
        # TODO : Factor in the 3d objects translation to origin constant
        cv2.circle(img, (circle[0], circle[1]), circle[2], (255, 0, 0), thickness=2, lineType=cv2.LINE_AA)
        centers_of_obstacles.append((circle[0], circle[1]))

    cv2.imshow("obstacles", img)
    cv2.waitKey(0)

    return centers_of_obstacles


def crop_environment(filename):
    im = cv2.imread(filename)

    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, treshold = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
    img_contours, contours, hierarchy = cv2.findContours(treshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

    for shape in contours:
        if len(shape) > 400:
            x, y, w, h = cv2.boundingRect(shape)
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
            crop_img = im[y:y + h, x:x + w]

    cv2.imshow('img', crop_img)
    cv2.waitKey(0)

    return crop_img


create_environment()
