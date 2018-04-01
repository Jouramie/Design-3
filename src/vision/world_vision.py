import cv2
import numpy as np

from src.domain.color import Color
from src.domain.vision_environment.cube import Cube
from src.domain.vision_environment.obstacle import Obstacle
from src.domain.vision_environment.target_zone import TargetZone
from src.domain.vision_environment.vision_environment import VisionEnvironment
from src.vision.vision_exception import VisionException

obstacle_file = '../fig/2018-02-10/obstacles10.jpg'

THICKNESS = 2


class DummyWorldVision:
    def __init__(self, camera):
        self.camera = camera

    def create_environment(self) -> VisionEnvironment:
        return VisionEnvironment([], [Obstacle((1043.5, 850.0), 52.9)],
                                 TargetZone((), []))  # TODO Hardcoder de quoi de plus complet


class WorldVision:
    def __init__(self):
        pass

    def create_environment(self, frame):
        # cropped_image = self.__crop_environment(image_location)
        # cropped_image_copy = copy.copy(cropped_image)

        cubes = []
        obstacles = []

        for cube in self.__find_color_cubes(frame, Color.BLUE):
            cubes.append(cube)

        for cube in self.__find_color_cubes(frame, Color.GREEN):
            cubes.append(cube)

        for cube in self.__find_color_cubes(frame, Color.RED):
            cubes.append(cube)

        for cube in self.__find_color_cubes(frame, Color.YELLOW):
            cubes.append(cube)

        for cube in self.__find_black_cubes(frame):
            cubes.append(cube)

        for cube in self.__find_white_cube(frame):
            cubes.append(cube)

        target_zone = self.__find_target_zone(frame)

        for obstacle in self.__find_obstacles(frame):
            obstacles.append(obstacle)

        return VisionEnvironment(cubes, obstacles, target_zone)

    def __find_color_cubes(self, original_image, color: Color):
        image = cv2.medianBlur(original_image, 5)
        image = cv2.GaussianBlur(image, (5, 5), 0)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, color.lower_bound, color.upper_bound)

        image_with_contours, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 400 > cv2.arcLength(contour, True) > 200:
                if (x > 1040 and y < 50) or (1450 < x) or (x > 1040 and y > 640):
                    yield self.__create_cube(contour, color)

    def __find_black_cubes(self, original_image):
        image = cv2.medianBlur(original_image, 5)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        kernel = np.ones((5, 5), np.uint8)

        image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        image = cv2.dilate(image, kernel, iterations=1)
        image = cv2.erode(image, kernel, iterations=1)

        _, thresh = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY_INV)
        image_with_contours, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if cv2.arcLength(contour, True) > 200:
                if (x > 1040 and y < 50) or (1450 < x) or (x > 1040 and y > 640):
                    yield self.__create_cube(contour, Color.BLACK)

    def __find_white_cube(self, original_image) -> [Cube]:
        image = cv2.medianBlur(original_image, 5)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, Color.WHITE.lower_bound, Color.WHITE.upper_bound)

        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 400 > cv2.arcLength(contour, True) > 100:
                if (x > 1040 and y < 50) or (1450 < x) or (x > 1040 and y > 640):
                    yield self.__create_cube(contour, Color.WHITE)

    def __create_cube(self, contour, color: Color) -> Cube:
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w / 2, y + h / 2)
        return Cube(center, color, [(x, y), (x + w, y + h)])

    def __find_target_zone(self, original_image) -> TargetZone:
        hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_image, Color.GREEN.lower_bound, Color.GREEN.upper_bound)

        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for shape in contours:
            x = shape[0][0][0]
            if cv2.arcLength(shape, True) > 2000 and x > 50:
                return self.__create_target_zone(shape)

    def __create_target_zone(self, contour) -> TargetZone:
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w / 2, y + h / 2)
        corners = [(x, y), (x + w, y + h)]
        return TargetZone(center, corners)

    def __find_obstacles(self, original_image) -> [Obstacle]:
        im = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

        im = cv2.GaussianBlur(im, (5, 5), 0)

        contours = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=50, maxRadius=80)

        if contours is not None:
            for contour in contours[0]:
                yield self.__create_obstacle(contour)

    def __create_obstacle(self, contour) -> Obstacle:
        center = (contour[0], contour[1])
        radius = contour[2]
        return Obstacle(center, radius)

    def __crop_environment(self, frame):
        original_image = frame

        image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(image, 127, 255, cv2.THRESH_TOZERO)
        image_with_contours, contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        crop_img = None

        for contour in contours:
            if cv2.arcLength(contour, True) > 3000:
                x, y, w, h = cv2.boundingRect(contour)
                crop_img = original_image[y:y + h, x:x + w]

        if crop_img is None:
            raise VisionException('Impossible to crop image.')

        return crop_img


if __name__ == "__main__":
    from src.vision.camera import create_camera

    cam = create_camera(1)
    frame = cam.take_picture()
    vision = WorldVision()
    env = vision.create_environment(frame)
    print(env)
