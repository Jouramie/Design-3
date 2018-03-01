import glob
import time
import os

import cv2

from src.vision.camera import create_camera
from vision.world_vision import WorldVision

camera_id = 1
camera = create_camera(camera_id)

capture = camera.take_picture()
cv2.imshow('capture', capture)

directory = '../../fig/' + time.strftime('%Y-%m-%d')
photo = glob.glob(directory + '/*.jpg')
demonstration = max(photo, key=os.path.getctime)

world_vision = WorldVision()
result = world_vision.create_environment(demonstration)
cv2.imshow('result', result[1])
if cv2.waitKey(0):
    cv2.destroyAllWindows()
