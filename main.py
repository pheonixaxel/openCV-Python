import os

import cv2 as cv
import numpy as np
import pyautogui

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def find_metin(metin_path, map_path, threshold=0.878, debug_mode=None):
    map_img = cv.imread(map_path)
    metin_img = cv.imread(metin_path)

    method = cv.TM_CCORR_NORMED
    result = cv.matchTemplate(map_img, metin_img, method)

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    print(locations)

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), metin_img.shape[1], metin_img.shape[0]]
        rectangles.append(rect)
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
    print(rectangles)

    points = []
    if len(rectangles) > 0:
        print('Found metin')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (x, y, w, h) in rectangles:
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)
            # Save the points
            points.append((center_x, center_y))

            if debug_mode == 'rectangles':
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                cv.rectangle(map_img, top_left, bottom_right, line_color, line_type, 2)

            elif debug_mode == 'points':
                cv.drawMarker(map_img, (center_x, center_y), marker_color, marker_type, 40, 2)

        if debug_mode:
            cv.imshow('Matches', map_img)
            cv.waitKey()

    return points


points = find_metin('screenshots/metin.png', 'screenshots/map.png', debug_mode='points')
print(points)
