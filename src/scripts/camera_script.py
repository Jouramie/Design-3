import cv2
import platform
import time
import os

world_camera_id = None

system = platform.system()
print('system {}'.format(system))
if  system == 'Linux':
    world_camera_id = 2
elif system == 'darwin':
    world_camera_id = 0
elif system == 'Windows':
    world_camera_id = 1

capture_object = cv2.VideoCapture(world_camera_id)
assert capture_object.isOpened(), "Erreur lors de l'ouverture"

for i in range(10):
    isFrameReturned, img = capture_object.read()

cv2.namedWindow('capture')
cv2.imshow('capture', img)

directory = "../../fig/" + time.strftime("%Y-%m-%d")
if not os.path.exists(directory):
    os.makedirs(directory)

cv2.imwrite(directory + time.strftime("/%Hh%M.jpg"), img)
cv2.waitKey()



