import os
from time import time

import cv2 as cv
import numpy as np
import pyautogui

from windowcapture import WindowCapture
from vision import Vision

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WindowCapture.list_window_names()

wincap = WindowCapture('Rodnia - The King\'s Return')
# metin_paths = ['screenshots/metin1.png', 'screenshots/metin2.png', 'screenshots/metin3.png', 'screenshots/metin4.png', 'screenshots/metin5.png']

vision = Vision('screenshots/metin.png')

loop_time = time()
while True:

    screenshot = wincap.get_screenshot()

    points = vision.find_metin(screenshot, debug_mode='rectangles')

    # cv.imshow('Metin2', screenshot)

    print('FPS{}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('done')
