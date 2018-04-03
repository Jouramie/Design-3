from logging import Logger

import cv2

from src.domain.environments.vision_environment import VisionEnvironment
from src.domain.objects.color import Color
from src.domain.objects.cube import Cube
from src.domain.objects.obstacle import Obstacle
from src.domain.objects.target_zone import TargetZone
from src.domain.table_crop import TableCrop

obstacle_file = '../fig/2018-02-10/obstacles10.jpg'

THICKNESS = 2


class MockedWorldVision:
    def create_environment(self) -> VisionEnvironment:
        return VisionEnvironment([], [Obstacle((1043.5, 850.0), 52.9)], TargetZone((), []))


class WorldVision:
    def __init__(self, logger: Logger, config: dict):
        self.logger = logger
        self.config = config

    def create_environment(self, frame, table):
        options = {1: TableCrop.TABLE1, 2: TableCrop.TABLE2, 4: TableCrop.TABLE4, 6: TableCrop.TABLE6}
        table_crop = options[table]
        cropped_image = self.__crop_environment(frame, table_crop)

        cubes = []
        obstacles = []

        cv2.imshow('frame', cropped_image)

        for cube in self.__find_red_cubes(cropped_image):
            cubes.append(cube)

        cubes = self.__validate_cube_is_present(cropped_image, Color.BLUE, cubes)
        cubes = self.__validate_cube_is_present(cropped_image, Color.GREEN, cubes)
        cubes = self.__validate_cube_is_present(cropped_image, Color.YELLOW, cubes)
        #cubes = self.__validate_cube_is_present(cropped_image, Color.BLACK, cubes)

        for cube in self.__find_color_cubes(cropped_image, Color.WHITE):
            cubes.append(cube)

        target_zone = self.__find_target_zone(cropped_image)

        for obstacle in self.__find_obstacles(cropped_image):
            obstacles.append(obstacle)

        for cube in cubes:
            cube.center = (cube.center[0], cube.center[1] + table_crop.y_crop_top)
            new_corners = []
            for corner in cube.corners:
                new_corners.append((corner[0], corner[1] + table_crop.y_crop_top))
            cube.corners = new_corners

        #self.__cube_list_validation(cubes, table_crop)
        #cubes = self.__cube_inside_cube_validation(cubes, table_crop)

        if target_zone is not None:
            target_zone.center = (target_zone.center[0], target_zone.center[1] + table_crop.y_crop_top)
            new_corners = []
            for corner in target_zone.corners:
                new_corners.append((corner[0], corner[1] + table_crop.y_crop_top))
            target_zone.corners = new_corners

        for obstacle in obstacles:
            obstacle.center = (int(obstacle.center[0]), int(obstacle.center[1] + table_crop.y_crop_top))

        return VisionEnvironment(cubes, obstacles, target_zone)

    # TODO vérifier que ça marche
    def __validate_cube_is_present(self, frame, color: Color, cubes):
        for cube in self.__find_color_cubes(frame, color):
            cubes.append(cube)
        for i in range(0, 2):
            for cube in cubes:
                if cube.color == color:
                    break
                else:
                    for cube in self.__find_color_cubes(frame, color):
                        cubes.append(cube)
        return cubes

    def __find_color_cubes(self, frame, color: Color):
        # image = cv2.medianBlur(frame, 5)
        # image = cv2.GaussianBlur(image, (5, 5), 0)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, color.lower_bound, color.upper_bound)

        image_with_contours, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        height, width, _ = frame.shape

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 500 > cv2.arcLength(contour, True) > 80:
                if ((0.8 * width < x < 0.92 * width) and (y <= 0.10 * height) or
                        ((0.96 * width < x < width) and (0.12 * height < y <= 0.82 * height)) or
                        ((0.78 * width < x < 0.92 * width) and (0.86 * height < y < height))):
                    yield self.__create_cube(contour, color)

    def __find_red_cubes(self, frame):
        red = Color.RED
        red2 = Color.RED2
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        red_mask = cv2.inRange(hsv, red.lower_bound, red.upper_bound)
        red2_mask = cv2.inRange(hsv, red2.lower_bound, red2.upper_bound)

        mask = red_mask + red2_mask

        image_with_contours, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        height, width, _ = frame.shape

        for contour in contours:
            x = contour[0][0][0]
            y = contour[0][0][1]
            if 500 > cv2.arcLength(contour, True) > 80:
                if ((0.8 * width < x < 0.92 * width) and (y <= 0.10 * height) or
                        ((0.96 * width < x < width) and (0.12 * height < y <= 0.82 * height)) or
                        ((0.78 * width < x < 0.92 * width) and (0.86 * height < y < height))):
                    yield self.__create_cube(contour, Color.RED)

    def __create_cube(self, contour, color: Color) -> Cube:
        x, y, w, h = cv2.boundingRect(contour)
        return Cube(color, [(x, y), (x + w, y + h)])

    def __find_target_zone(self, original_image) -> TargetZone:
        hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_image, Color.TARGET_ZONE_GREEN.lower_bound, Color.TARGET_ZONE_GREEN.upper_bound)

        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for shape in contours:
            x = shape[0][0][0]
            if cv2.arcLength(shape, True) > 2000 and x > 50:
                return self.__create_target_zone(shape)
            else:
                break

        hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_image, Color.GREEN.lower_bound, Color.GREEN.upper_bound)

        img, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for shape in contours:
            x = shape[0][0][0]
            if cv2.arcLength(shape, True) > 3000 and x > 50:
                return self.__create_target_zone(shape)
            else:
                break

    def __create_target_zone(self, contour) -> TargetZone:
        x, y, w, h = cv2.boundingRect(contour)
        center = (x + w / 2, y + h / 2)
        corners = [(x, y), (x + w, y + h)]
        return TargetZone(center, corners)

    def __find_obstacles(self, frame) -> [Obstacle]:
        im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        height, width, _ = frame.shape

        im = cv2.GaussianBlur(im, (5, 5), 0)

        contours = cv2.HoughCircles(im, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=50, maxRadius=60)

        if contours is not None:
            for contour in contours[0]:
                x = contour[0]
                if x > 0.4 * width:
                    print(width)
                    print(x)
                    yield self.__create_obstacle(contour)

    def __create_obstacle(self, contour) -> Obstacle:
        center = (contour[0], contour[1])
        radius = contour[2]
        return Obstacle(center, radius)

    def __crop_environment(self, frame, table_crop):
        x = 0
        w = 1600 - table_crop.x_crop
        y = table_crop.y_crop_top
        h = 1200 - table_crop.y_crop_top - table_crop.y_crop_bot

        crop_img = frame[y:y + h, x:x + w]

        return crop_img

    def __cube_list_validation(self, cubes: [Cube], table_crop: TableCrop):
        for cube in cubes:
            print(cube)
            for another_cube in cubes:
                if another_cube != cube:
                    if cube.is_too_close(another_cube) and cube.color == another_cube.color:
                        merged_cube = cube.merge(another_cube, table_crop)
                        cubes.append(merged_cube)
                        if cube in cubes:
                            cubes.remove(cube)
                        if another_cube in cubes:
                            cubes.remove(another_cube)
                    elif cube.is_too_close(another_cube) and another_cube.color == Color.WHITE:
                        if another_cube in cubes:
                            cubes.remove(another_cube)
        return cubes

    def __cube_inside_cube_validation(self, cubes: [Cube], table_crop: TableCrop):
        for cube in cubes:
            for another_cube in cubes:
                if another_cube != cube:
                    if another_cube.is_inside(cube):
                        if another_cube.color == Color.WHITE and cube.color != Color.WHITE:
                            cubes.remove(another_cube)
                        if cube.get_color() == another_cube.get_color():
                            merged_cube = cube.merge_center(another_cube, table_crop)
                            merged_cube.set_color(cube.get_color())
                            cubes.append(merged_cube)
                            if cube in cubes:
                                cubes.remove(cube)
                            if another_cube in cubes:
                                cubes.remove(another_cube)
        return cubes

    def __cube_too_close_validation(self, cubes: [Cube]):
        for cube in cubes:
            for another_cube in cubes:
                print('hello')
