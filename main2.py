import os
from time import time

import cv2 as cv
import numpy as np
import pyautogui

from windowcapture import WindowCapture

os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture('Rodnia - The King\'s Return')

loop_time = time()
while(True):

    screenshot = wincap.get_screenshot()

    cv.imshow('Metin2', screenshot)

    print('FPS{}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('done')