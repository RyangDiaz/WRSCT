import cv2
import numpy as np
import matplotlib.pyplot as plt

def hsv_thresh(img):
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
    # cv2.imshow('orig', img)
    display_img(total_thresh)
    return total_thresh

def find_contours(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contour_img = cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0,255,0), thickness=2)
    display_img(contour_img)
    return contours #Returns list 

    
# For use in image display and debugging
def display_img(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    

#For later use in vector plotting
def plot_point(filepath, x, y):
    img = cv2.imread(filepath)
    img = cv2.circle(img, (x, y), radius=10, color=(0, 0, 255), thickness=-1)
    cv2.imshow('plotted', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    filepath = 'radar.jpg'
    img = cv2.imread(filepath)
    display_img(img)
    threshed = hsv_thresh(img)
    contours = find_contours(threshed)
    orig_contours = cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0,255,0), thickness=2)
    display_img(orig_contours)


