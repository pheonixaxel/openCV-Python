import os
import numpy as np
from time import time

import cv2 as cv
from hsvfilter import HsvFilter

from windowcapture import WindowCapture
# from vision import Vision

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
wincap = WindowCapture('Rodnia - The King\'s Return')
# initialize the Vision class
# vision = Vision('screenshots/metin.png')
# initialize the trackbar window
# vision.init_control_gui()

# metin_paths = ['screenshots/metin1.png', 'screenshots/metin2.png', 'screenshots/metin3.png',
# 'screenshots/metin4.png', 'screenshots/metin5.png']



# # initialize the trackbar window
# hsv_filter = HsvFilter(0, 180, 129, 179, 255, 255, 0, 0, 67, 0)

loop_time = time()
while True:

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # pre-process the image
    # processed_image = vision.apply_hsv_filter(screenshot)

    # do object detection
    # rectangles = vision.find_metin(processed_image)

    # draw the detection results onto the original image
    # output_image = vision.draw_rectangles(screenshot, rectangles)

    # cv.imshow('Processed', processed_image)
    # cv.imshow('Matches', output_image)

    cv.imshow('Unprocessed', screenshot)

    # debug the loop rate
    print('FPS{}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('f'):
        cv.imwrite('positive/{}.png'.format(loop_time), screenshot)
    elif key == ord('d'):
        cv.imwrite('negative/{}.png'.format(loop_time), screenshot)

print('done')


