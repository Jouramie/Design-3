import cv2
import argparse

from src.vision.worldCamera import WorldCamera


def main(number, camera_id):
    worldcam = WorldCamera(camera_id, None)
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