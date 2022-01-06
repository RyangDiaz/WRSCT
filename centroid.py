import cv2
import numpy as np
import matplotlib.pyplot as plt
import imageio
import urllib.request
import os

## Important color tuples and constant values
struct_ele_size = (3, 3) # For detail/cell blurring and line removal

yellow_lower = (15, 90, 90)
yellow_higher = (36, 255, 255)
red_lower_A = (0, 120, 120) # Red range wraps across HSV value boundaries for Hue
red_higher_A = (10, 255, 255)
red_lower_B = (170, 120, 120)
red_higher_B = (180, 255, 255)
blue_lower = (90, 200, 200)
blue_higher = (115, 255, 255)

#====================== Functions to write ======================#

# Merge together groups of smaller cells, simplifies general shape of cells
def simplify_img(img):
    pass

# Removes county/state lines in colored cells, returns a modified mask (binary image)
def remove_lines(img):
    # Kernel shape is a cross due to rigid horizontal/vertical nature of borders
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, struct_ele_size)
    removed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return removed

# Isolates cells of interest, returns storm cell shapes for contour detection purposes
def hsv_thresh(img):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Creating components of color mask (include red, yellow, and blue colors)
    yel_thresh = cv2.inRange(hsv_img, yellow_lower, yellow_higher)
    red_thresh1 = cv2.inRange(hsv_img, red_lower_A, red_higher_A)
    red_thresh2 = cv2.inRange(hsv_img, red_lower_B, red_higher_B)
    blu_thresh = cv2.inRange(hsv_img, blue_lower, blue_higher)

    mask = remove_lines(yel_thresh + red_thresh1 + red_thresh2 + blu_thresh)
    return mask

# Finds contours of cells of interest [Assume that input image is already binary]
# Returns a list of relevant contours in the image
def find_contours(img):
    # Finds all contours of image 
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    # Remove smaller contours to reduce number of relevant cells
    acceptable_contours = []
    for contour in contours:
        if cv2.contourArea(contour) > 50: # Arbitrary threshold, determined through testing 
            acceptable_contours.append(contour)
    
    return acceptable_contours

    
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
    # Default: Saint Paul, MN Intellicast Radar ("stc")
    locations = {
        "California": "bfl",
        "New York": "bgm",
        "New Hampshire": "bml",
        "Texas": "bro",
        "Kentucky": "bwg",
        "Michigan": "cad",
        "North Carolina": "clt",
        "Georgia": "csg",
        "Ohio": "day",
        "Colorado": "den",
        "Iowa": "dsm",
        "Florida": "pie",
        "Virginia": "fcx",
        "Connecticut": "hfd",
        "Missouri": "jef",
        "Oklahoma": "law",
        "Nebraska": "lbf",
        "Arkansas": "lit",
        "Louisiana": "msy",
        "Idaho": "myl",
        "South Dakota": "pir",
        "Arizona": "prc",
        "Utah": "pvu",
        "Oregon": "rdm",
        "Wyoming": "riw",
        "Nevada": "rno",
        "New Mexico": "row",
        "Kansas": "sln",
        "Illinois": "spi",
        "Minnesota": "stc",
        "Washington": "tiw",
        "Mississippi": "tvr"
        }
    state = "Minnesota"
    url = "https://s.w-x.co/staticmaps/wu/wxtype/county_loc/{}/animate.png".format(locations[state])
    fname = "radarloop.gif"

    # Read the gif from the web, save to the disk
    imdata = urllib.request.urlopen(url).read()
    open(fname, "wb+").write(imdata)

    # Read the gif from disk to `RGB`s using `imageio.miread`
    gif = imageio.mimread(fname)
    
    # Remove written file - May not remove depending on working directory of program
    os.remove(fname)
    nums = len(gif)
    print("Total {} frames in the gif!".format(nums), "\nCurrent Location:", state)

    # Convert form RGB to BGR 
    imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]

    # Crop top part out of images
    for i in range(len(imgs)):
        imgs[i] = imgs[i][22:, :]
    
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


