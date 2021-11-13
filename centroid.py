import cv2
import numpy as np
import matplotlib.pyplot as plt
import imageio
import urllib.request
import os

### For testing purposes
import copy
###^^^^^

#====================== Functions to write ======================#

## Merge together groups of smaller cells, simplifies general shape of cells 
def simplify_img(img):
    pass




# Removes county/state lines in colored cells, returns a modified mask (binary image)
def remove_lines(img):
    # Kernel shape is a cross due to rigid horizontal/vertical nature of borders
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))

    # Closing = Dilation + Erosion
    removed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    
    return removed

# Isolates cells of interest, returns storm cell shapes for contour detection purposes
def hsv_thresh(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    ## mask of yellow (15,0,0) ~ (36, 255, 255)
    # Modified values of S and V to avoid including background
    yel_thresh = cv2.inRange(hsv_img, (15,90,90), (36,255,255)) 
    ## mask of red (0, 0, 0) ~ (10, 255, 255) AND (170, 0, 0) ~ (180, 255, 255)
    red_thresh1 = cv2.inRange(hsv_img, (0,120,120), (10,255,255))
    red_thresh2 = cv2.inRange(hsv_img, (170,120,120), (180,255,255))
    ## mask of blue (100,0,0) ~ (140, 255, 255)
    blu_thresh = cv2.inRange(hsv_img, (90,200,200), (115,255,255))
    
    # Total mask for yellow and red colors
    mask = remove_lines(yel_thresh + red_thresh1 + red_thresh2 + blu_thresh)
    
    
    # Converts binary image back into portions of original image
    #total_thresh = cv2.bitwise_and(img, img, mask=mask)

    ## Display image (for testing purposes)
    '''
    display_img(total_thresh)
    '''
    ###^^^
    
    return mask

# Finds contours of cells of interest (should call hsv_thresh first) [EDIT: Assume that input image is already binary]
def find_contours(img):
    
    ###### For testing purposes (display original contours) - Used to determine size threshold
    #other_img = copy.deepcopy(img)
    ######^^^^^

    # Image preprocessing for contour finding
    #gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #th, thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY)

    # Finds all contours of image 
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    ## For testing purposes (display original contours)
    #before_contour_img = cv2.drawContours(image=other_img, contours=contours, contourIdx=-1, color=(0,255,0), thickness=2)
    #display_img(before_contour_img)
    ######^^^^
    
    # Remove smaller contours to reduce number of relevant cells
    acceptable_contours = []
    for contour in contours:
        if cv2.contourArea(contour) > 50: # Arbitrary threshold, determined through testing 
            acceptable_contours.append(contour)

    ## Displays image (for testing purposes)
    '''
    contour_img = cv2.drawContours(image=img, contours=acceptable_contours, contourIdx=-1, color=(0,255,0), thickness=2)
    display_img(contour_img)
    '''
    ###^^^^^
    
    return acceptable_contours # Returns list

    
# For use in image display and debugging
def display_img(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

# For later use in vector plotting
def plot_point(img, x, y):
    img = cv2.circle(img, (x, y), radius=10, color=(0, 0, 255), thickness=-1)
    display_img(img)
    return img

# Prototype for scraping image files
def read_image():
    # Default: Saint Paul, MN Intellicast Radar 
    url = "https://s.w-x.co/staticmaps/wu/wxtype/county_loc/stc/animate.png"
    #url = "https://s.w-x.co/staticmaps/wu/wxtype/county_loc/cad/animate.png"
    fname = "test.gif"

    ## Read the gif from the web, save to the disk
    imdata = urllib.request.urlopen(url).read()
    imbytes = bytearray(imdata)
    open(fname,"wb+").write(imdata)

    ## Read the gif from disk to `RGB`s using `imageio.miread` 
    gif = imageio.mimread(fname)
    
    # Remove written file - May not remove depending on working directory of program
    os.remove(fname)
    nums = len(gif)
    print("Total {} frames in the gif!".format(nums))

    # Convert form RGB to BGR 
    imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]

    # Crop top part out of images
    for i in range(len(imgs)):
        imgs[i] = imgs[i][22:,:]
    
    return imgs

if __name__ == '__main__':
    response = input("For testing purposes: input image? (y/n): ")
    if response.lower() == "y":
        filepath = input('Name of img: ')
        img = cv2.imread(filepath)
        display_img(img)
        threshed = hsv_thresh(img)
        contours = find_contours(threshed)
        orig_contours = cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0,255,0), thickness=2)
        display_img(orig_contours)
    else:
        frames = read_image()
        for frame in frames:
            threshed = hsv_thresh(frame)
            contours = find_contours(threshed)
            orig_contours = cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(0,255,0), thickness=2)
            display_img(orig_contours)


