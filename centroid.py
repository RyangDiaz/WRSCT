import cv2
gray_image = cv2.imread("/Users/ryandiaz/Documents/WRSCT/radar_img_2.jpg", cv2.IMREAD_GRAYSCALE)
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



