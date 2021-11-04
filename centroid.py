import cv2
import numpy as np
import matplotlib.pyplot as plt

#Original threshold processing
def bw_threshold(filepath):
    gray_image = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    background_thresh = 211
    cell_thresh = 195
    maxValue = 255

    #Remove background - threshold based on color instead?
    th, dst = cv2.threshold(gray_image, background_thresh, maxValue, cv2.THRESH_TOZERO_INV)

    #Isolate yellow cells
    th2, dst2 = cv2.threshold(dst, cell_thresh, maxValue, cv2.THRESH_BINARY)
    cv2.imshow('oldimg', gray_image)
    cv2.imshow('newimg', dst2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def hsv_thresh(filepath):
    img = cv2.imread(filepath)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    ## mask of yellow (15,0,0) ~ (36, 255, 255)
    # Modified values of S and V to avoid including background
    yel_thresh = cv2.inRange(hsv_img, (15,90,90), (36,255,255)) 
    ## mask of red (0, 0, 0) ~ (10, 255, 255) AND (170, 0, 0) ~ (180, 255, 255)
    red_thresh1 = cv2.inRange(hsv_img, (0,120,120), (10,255,255))
    red_thresh2 = cv2.inRange(hsv_img, (170,120,120), (180,255,255))
    # Total mask for yellow and red colors
    mask = yel_thresh + red_thresh1 + red_thresh2
    #Converts binary image back into portions of original image
    total_thresh = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow('orig', img)
    cv2.imshow('result', total_thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#For later use in vector plotting
def plot_point(filepath, x, y):
    img = cv2.imread(filepath)
    img = cv2.circle(img, (x, y), radius=10, color=(0, 0, 255), thickness=-1)
    cv2.imshow('plotted', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



