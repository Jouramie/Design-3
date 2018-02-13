import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

nx = 7  # TODO: enter the number of inside corners in x
ny = 7  # TODO: enter the number of inside corners in y

# Make a list of calibration images
images = glob.glob('../../fig/2018-02-12/*.jpg')


for i in images:
    print('-> processing image {}'.format(i))
    img = cv2.imread(i)
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

    # If found, draw corners
    if ret == True:
        # Draw and display the corners
        cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
        cv2.imshow('yoyo', img)
        plt.imshow(img)
        plt.show()


cv2.waitKey()
cv2.destroyAllWindows()

