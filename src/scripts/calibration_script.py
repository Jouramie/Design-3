import cv2
import argparse

from vision.camera import create_camera


def main(number, camera_id):
    worldcam = create_camera(camera_id)
    for i in range(number):
        input("Press any key\n")
        worldcam.take_picture()
    worldcam.capture_object.release()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, help="number of picture to be taken")
    args = parser.parse_args()

    camera_id = 1
    main(args.number, camera_id)