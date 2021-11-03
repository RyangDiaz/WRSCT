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
    ## mask of yellow (15,0,0) ~ (36, 255, 255)
    img = cv2.imread(filepath)
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow('orig', img)
    #Modified values of S and V to avoid including background
    thresh = cv2.inRange(hsv_img, (15,90,90), (36,255,255))
    cv2.imshow('threshed', thresh)
    #Converts binary image back into portions of original image 
    yel_mask = cv2.bitwise_and(img, img, mask=thresh)
    cv2.imshow('yells', yel_mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#For later use in vector plotting
def plot_point(filepath, x, y):
    img = cv2.imread(filepath)
    img = cv2.circle(img, (x, y), radius=10, color=(0, 0, 255), thickness=-1)
    cv2.imshow('iwannadie', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



