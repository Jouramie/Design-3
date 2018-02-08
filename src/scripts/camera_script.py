import cv2
import platform

world_camera_id = None

system = platform.system()
if  system == 'Linux':
    world_camera_id = 2
elif system == 'darwin':
    world_camera_id = 0
elif system == 'win32' or system == 'win64':
    world_camera_id = 0

capture_object = cv2.VideoCapture(world_camera_id)
assert capture_object.isOpened(), "Erreur lors de l'ouverture"

for i in range(10):
    isFrameReturned, img = capture_object.read()

cv2.namedWindow('capture')
cv2.imshow('capture', img)
cv2.imwrite("capture.png", img)
cv2.waitKey()



