import cv2 as cv
import numpy as np
from hsvfilter import HsvFilter


class Vision:
    # constants
    TRACKBAR_WINDOW = "Trackbars"

    # properties
    metin_img = None
    metin_w = 0
    metin_h = 0
    method = None

    # constructor
    # def __init__(self, metin_path, method=cv.TM_CCORR_NORMED):
    #
    #     # load the metin image
    #     self.metin_img = cv.imread(metin_path, cv.IMREAD_UNCHANGED)
    #
    #     # self.metin_img = self.metin_img[..., :3]
    #
    #     # print the found image shape
    #     # print(self.metin_img.shape)
    #
    #     # Save the dimensions of the metin image
    #     self.metin_w = self.metin_img.shape[1]
    #     self.metin_h = self.metin_img.shape[0]
    #
    #     self.method = method

    def __init__(self, metin_path, method=cv.TM_CCORR_NORMED):
        # Load the metin image as a 3-channel (color) image with depth CV_8U
        self.metin_img = cv.imread(metin_path, cv.IMREAD_COLOR)

        # Verify that the image was loaded successfully
        if self.metin_img is None:
            raise ValueError(f"Failed to load image from {metin_path}")

        # Save the dimensions of the metin image
        self.metin_w = self.metin_img.shape[1]
        self.metin_h = self.metin_img.shape[0]

        self.method = method

    def find_metin(self, map_img, threshold=0.87, max_results=5):

        # perform the template matching - OpenCV algorithm
        result = cv.matchTemplate(map_img, self.metin_img, self.method)

        # get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        # print(locations)

        # if we found no matches, return now. this reshapes of the empty array allows us to
        # concatenate together results without causing an error
        if not locations:
            return np.array([], dtype=np.int32).reshape(0, 4)

        # group the (x, y) coordinates from the rectangle corners
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.metin_w, self.metin_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)

        # apply group rectangles
        # The groupRectangles() function simply does the job of merging overlapping rectangles.
        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)
        # print(rectangles)

        # for performance reasons, return a limited number of results
        # these are not necessarily the best results
        if len(rectangles) > max_results:
            print('Warning: too many results, raise the threshold.')
            rectangles = rectangles[:max_results]

        return rectangles

    # This function will return the center points of the rectangles
    def get_click_points(self, rectangles):
        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
            # Determine the center position
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)
            # Save the points
            points.append((center_x, center_y))

        return points

    # This function will draw the rectangles on the map image
    def draw_rectangles(self, map_img, rectangles):

        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for (x, y, w, h) in rectangles:
            # Determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # Draw the box
            cv.rectangle(map_img, top_left, bottom_right, line_color, line_type, 2)

        return map_img

    # This function will draw the points on the map image
    def draw_points(self, map_img, points):

        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (center_x, center_y) in points:
            # Draw the center point
            cv.drawMarker(map_img, (center_x, center_y), marker_color, marker_type, 40, 2)

        return map_img

    def init_control_gui(self):
        cv.namedWindow(self.TRACKBAR_WINDOW, cv.WINDOW_NORMAL)
        cv.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        # required callback. we'll be using getTrackbarPos() to do lookups
        # instead of using the callback.
        def nothing(position):
            pass

        # create trackbars for bracketing.
        # OpenCV scale for HSV is H: 0-179, S: 0-255, V: 0-255
        cv.createTrackbar('HMin', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMin', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('HMax', self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv.createTrackbar('SMax', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VMax', self.TRACKBAR_WINDOW, 0, 255, nothing)

        # Set default value for Max HSV trackbars
        cv.setTrackbarPos('HMax', self.TRACKBAR_WINDOW, 179)
        cv.setTrackbarPos('SMax', self.TRACKBAR_WINDOW, 255)
        cv.setTrackbarPos('VMax', self.TRACKBAR_WINDOW, 255)

        # trackbars for increasing/decreasing saturation and value
        cv.createTrackbar('SAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('SSub', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VAdd', self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv.createTrackbar('VSub', self.TRACKBAR_WINDOW, 0, 255, nothing)

    # returns an HSV filter object based on the control GUI values
    def get_hsv_filter_from_controls(self):
        # Get current positions of all trackbars
        hsv_filter = HsvFilter()
        hsv_filter.hMin = cv.getTrackbarPos('HMin', self.TRACKBAR_WINDOW)
        hsv_filter.sMin = cv.getTrackbarPos('SMin', self.TRACKBAR_WINDOW)
        hsv_filter.vMin = cv.getTrackbarPos('VMin', self.TRACKBAR_WINDOW)
        hsv_filter.hMax = cv.getTrackbarPos('HMax', self.TRACKBAR_WINDOW)
        hsv_filter.sMax = cv.getTrackbarPos('SMax', self.TRACKBAR_WINDOW)
        hsv_filter.vMax = cv.getTrackbarPos('VMax', self.TRACKBAR_WINDOW)
        hsv_filter.sAdd = cv.getTrackbarPos('SAdd', self.TRACKBAR_WINDOW)
        hsv_filter.sSub = cv.getTrackbarPos('SSub', self.TRACKBAR_WINDOW)
        hsv_filter.vAdd = cv.getTrackbarPos('VAdd', self.TRACKBAR_WINDOW)
        hsv_filter.vSub = cv.getTrackbarPos('VSub', self.TRACKBAR_WINDOW)
        return hsv_filter

    def apply_hsv_filter(self, original_image, hsv_filter=None):
        # convert image to HSV
        hsv = cv.cvtColor(original_image, cv.COLOR_BGR2HSV)

        # if we haven't been given a defined filter, use the filter values from the GUI
        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        # add/subtract saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        return img

    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c


'''
points = find_metin('screenshots/metin.png', 'screenshots/map.png', debug_mode='points')
print(points)

import os
import cv2 as cv
import numpy as np
import pyautogui

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class Vision:

    metin_imgs = []
    metin_ws = []
    metin_hs = []
    method = None

    def __init__(self, metin_paths, method=cv.TM_CCORR_NORMED):

        for path in metin_paths:
            metin_img = cv.imread(path, cv.IMREAD_UNCHANGED)
            metin_img = metin_img[..., :3]

            self.metin_imgs.append(metin_img)
            self.metin_ws.append(metin_img.shape[1])
            self.metin_hs.append(metin_img.shape[0])

        self.method = method

    def find_metin(self, map_img, threshold=0.878, debug_mode=None):

        points = []

        for metin_img, metin_w, metin_h in zip(self.metin_imgs, self.metin_ws, self.metin_hs):
            result = cv.matchTemplate(map_img, metin_img, self.method)

            locations = np.where(result >= threshold)
            locations = list(zip(*locations[::-1]))
            print(locations)

            rectangles = []
            for loc in locations:
                rect = [int(loc[0]), int(loc[1]), metin_w, metin_h]
                rectangles.append(rect)
                rectangles.append(rect)

            rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

            line_color = (0, 255, 0)
            line_type = cv.LINE_4

            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            if len(rectangles) > 0:
                print('Found metin')

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
        return points


# Usage example:
metin_paths = ['screenshots/metin1.png', 'screenshots/metin2.png', 'screenshots/metin3.png']
vision = Vision(metin_paths, method=cv.TM_CCORR_NORMED)
map_img = cv.imread('screenshots/map.png')
detected_points = vision.find_metin(map_img, debug_mode='points')
print(detected_points)
'''
