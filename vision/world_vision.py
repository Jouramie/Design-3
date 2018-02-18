import cv2
from matplotlib import pyplot as plt
from vision.hsv_enum import *

image_file = '../fig/2018-02-10/16h42.png';
cap = cv2.VideoCapture(0)


def create_environment():
    while (1):
        _, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        res = cv2.bitwise_and(frame, frame, mask=mask)

        cv2.imshow('frame', frame)
        cv2.imshow('mask', mask)
        cv2.imshow('res', res)
        k = cv2.waitKey(5) & 0xFF
        if k == 1:
            break
    cv2.destroyAllWindows()


def edge_detection():
    img = cv2.imread('../fig/2018-02-10/13h15.png', 0)
    edges = cv2.Canny(img, 100, 200)

    plt.subplot(121), plt.imshow(img, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(edges, cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()


def apply_mask_to_image(filename):
    im = cv2.imread(filename)
    shapes = []

    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    print(type(lower_blue))

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE);

    for shape in contours:
        if 200 > len(shape) > 40 and shape[0][0][0] > 600:
            x, y, w, h = cv2.boundingRect(shape)
            cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
            shapes.append(shape)

    cv2.imshow('frame', im)
    k = cv2.waitKey(0)


apply_mask_to_image(image_file)





