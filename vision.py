import os

import cv2 as cv
import numpy as np
import pyautogui

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Vision:

    metin_img = None
    metin_w = 0
    metin_h = 0
    method = None

    def __init__(self, metin_path, method=cv.TM_CCORR_NORMED):

        self.metin_img = cv.imread(metin_path, cv.IMREAD_UNCHANGED)
        self.metin_img = self.metin_img[..., :3]

        # print the found image shape
        # print(self.metin_img.shape)

        self.metin_w = self.metin_img.shape[1]
        self.metin_h = self.metin_img.shape[0]

        self.method = method

    def find_metin(self, map_img, threshold=0.878, debug_mode=None):

        result = cv.matchTemplate(map_img, self.metin_img, self.method)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        print(locations)

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.metin_img.shape[1], self.metin_img.shape[0]]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
        # print(rectangles)

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
        #       cv.waitKey()
        return points

# points = find_metin('screenshots/metin.png', 'screenshots/map.png', debug_mode='points')
# print(points)

# import os
# import cv2 as cv
# import numpy as np
# import pyautogui
#
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
#
#
# class Vision:
#
#     metin_imgs = []
#     metin_ws = []
#     metin_hs = []
#     method = None
#
#     def __init__(self, metin_paths, method=cv.TM_CCORR_NORMED):
#
#         for path in metin_paths:
#             metin_img = cv.imread(path, cv.IMREAD_UNCHANGED)
#             metin_img = metin_img[..., :3]
#
#             self.metin_imgs.append(metin_img)
#             self.metin_ws.append(metin_img.shape[1])
#             self.metin_hs.append(metin_img.shape[0])
#
#         self.method = method
#
#     def find_metin(self, map_img, threshold=0.878, debug_mode=None):
#
#         points = []
#
#         for metin_img, metin_w, metin_h in zip(self.metin_imgs, self.metin_ws, self.metin_hs):
#             result = cv.matchTemplate(map_img, metin_img, self.method)
#
#             locations = np.where(result >= threshold)
#             locations = list(zip(*locations[::-1]))
#             print(locations)
#
#             rectangles = []
#             for loc in locations:
#                 rect = [int(loc[0]), int(loc[1]), metin_w, metin_h]
#                 rectangles.append(rect)
#                 rectangles.append(rect)
#
#             rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
#
#             line_color = (0, 255, 0)
#             line_type = cv.LINE_4
#
#             marker_color = (255, 0, 255)
#             marker_type = cv.MARKER_CROSS
#
#             if len(rectangles) > 0:
#                 print('Found metin')
#
#                 for (x, y, w, h) in rectangles:
#                     center_x = x + int(w / 2)
#                     center_y = y + int(h / 2)
#                     # Save the points
#                     points.append((center_x, center_y))
#
#                     if debug_mode == 'rectangles':
#                         top_left = (x, y)
#                         bottom_right = (x + w, y + h)
#                         cv.rectangle(map_img, top_left, bottom_right, line_color, line_type, 2)
#
#                     elif debug_mode == 'points':
#                         cv.drawMarker(map_img, (center_x, center_y), marker_color, marker_type, 40, 2)
#
#         if debug_mode:
#             cv.imshow('Matches', map_img)
#         return points
#
#
# # Usage example:
# metin_paths = ['screenshots/metin1.png', 'screenshots/metin2.png', 'screenshots/metin3.png']
# vision = Vision(metin_paths, method=cv.TM_CCORR_NORMED)
# map_img = cv.imread('screenshots/map.png')
# detected_points = vision.find_metin(map_img, debug_mode='points')
# print(detected_points)