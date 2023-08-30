import os

import cv2 as cv
import numpy as np
import pyautogui


os.chdir(os.path.dirname(os.path.abspath(__file__)))

map_img = cv.imread('screenshots/map.png')
metin_stone_img = cv.imread('screenshots/metin.png')

result = cv.matchTemplate(map_img, metin_stone_img, cv.TM_CCORR_NORMED)

threshold = 0.878
locations = np.where(result >= threshold)
print(locations)

locations = list(zip(*locations[::-1]))
print(locations)


if locations:
    print('Found metin stone')

    metin_w = metin_stone_img.shape[1]
    metin_h = metin_stone_img.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    # Loop over all the locations and draw their rectangle
    for loc in locations:
        # Determine the box positions
        top_left = loc
        bottom_right = (top_left[0] + metin_w, top_left[1] + metin_h)
        # Draw the box
        cv.rectangle(map_img, top_left, bottom_right, line_color, line_type)

    cv.imshow('Matches', map_img)
    cv.waitKey()


#
# # get the best match position
# min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
#
# # pyautogui.rightClick(min_loc[0], min_loc[1])
#
# print('Best match top left position: %s' % str(max_loc))
# print('Best match confidence: %s' % max_val)
# print('--------------------------')
# print('Least match top left position: %s' % str(min_loc))
# print('Least match confidence: %s' % min_val)
#
# threshold = 0.8
# if max_val >= threshold:
#     print('Found metin stone')
#
#     top_left = max_loc
#     bottom_right = (top_left[0] + metin_stone_img.shape[1], top_left[1] + metin_stone_img.shape[0])
#
#     cv.rectangle(map_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)
#     cv.imshow('result', map_img)
#     cv.waitKey()
#
# else:
#     print('Metin stone not found')
