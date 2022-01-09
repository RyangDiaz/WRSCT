# Calculates and displays contours on radar images

import cv2
import radar_scrape as rs

# Important color tuples and constant values
STRUCT_ELE_SIZE = (3, 3)  # For detail/cell blurring and line removal
CONTOUR_THRESHOLD = 50

yellow_lower = (15, 90, 90)
yellow_higher = (36, 255, 255)
red_lower_A = (0, 120, 120)  # Red range wraps across HSV value boundaries for Hue
red_higher_A = (10, 255, 255)
red_lower_B = (170, 120, 120)
red_higher_B = (180, 255, 255)
blue_lower = (90, 200, 200)
blue_higher = (115, 255, 255)


# Merge together groups of smaller cells, simplifies general shape of cells
def simplify_img(img):
    pass

def find_centroids(contours):
    centroids = []
    for contour in contours:
        moment = cv2.moments(contour)
        # Tuple of x and y coords of centroid
        centroids.append((int(moment['m10']/moment['m00']), int(moment['m01']/moment['m00'])))
    return centroids

# Removes county/state lines in colored cells, returns a modified mask (binary image)
def remove_lines(img):
    # Kernel shape is a cross due to rigid horizontal/vertical nature of borders
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, STRUCT_ELE_SIZE)
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
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Remove smaller contours to reduce number of relevant cells
    acceptable_contours = []
    for contour in contours:
        if cv2.contourArea(contour) > CONTOUR_THRESHOLD:  # Arbitrary threshold, determined through testing
            acceptable_contours.append(contour)

    return acceptable_contours


# For use in image display and debugging
def display_img(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# For later use in vector plotting
def plot_point(img, x, y, color=True):
    if color:
        cv2.circle(img, (x, y), radius=5, color=(0, 0, 255), thickness=-1)
    else:
        cv2.circle(img, (x, y), radius=5, color=(255, 0, 0), thickness=-1)

def main():
    if __name__ == '__main__':
        response = input("Input name of state (default MN): ")
        frames = rs.read_image(response)
        # Convert form RGB to BGR
        frames = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in frames]  # VERY IMPORTANT
        for frame in frames:
            threshed = hsv_thresh(frame)
            contours = find_contours(threshed)
            centroids = find_centroids(contours)
            cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2)
            for centroid in centroids:
                plot_point(frame, centroid[0], centroid[1])
        while(True):
            for frame in frames:
                cv2.imshow('radar', frame)
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    exit(0)

if __name__ == '__main__':
    main()
