import numpy as np
import imutils
import cv2

# Directions:
# Use the color.py script to determine the HSV values of the ball in the scene
# Code them into this script as orangeLower and orangeUpper
# Take three screen shots at different distances, and measure each distance from camera to ball.
# Measure the ball's radius in real life
# Hard-code the KNOWN_DISTANCE (for the first image) and the KNOWN_WIDTH for the ball's radius
# Run this script and see what the focal length is. Also make sure that its output matches the measured data.
# Once you have the focal length, you can use that for the main.py script

#RGB values:
#(0, 165, 206)
#(148, 255, 255)
def find_marker_radius(image):
    # White
    #orangeLower = (51, 0, 149)
    #orangeUpper = (105, 57, 255)

    # Orange
    orangeLower = (25, 0, 239)
    orangeUpper = (36, 255, 255)
    print "Showing image in a frame, push a key to move on"
    frame = cv2.imshow("Frame", image)

    cv2.waitKey(0)
    print "Converting image to hsv"
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    cv2.imshow("Frame", hsv)
    cv2.waitKey(0)

    print "Masking for the right color"
    mask = cv2.inRange(hsv, orangeLower, orangeUpper)

    cv2.imshow("Frame", mask)
    cv2.waitKey(0)

    print "Masking by eroding"
    mask = cv2.erode(mask, None, iterations=2)

    cv2.imshow("Frame", mask)
    cv2.waitKey(0)

    print "Dilating"
    mask = cv2.dilate(mask, None, iterations=2)

    cv2.imshow("Frame", mask)
    cv2.waitKey(0)

    print "Finding contours"
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(radius), (0, 100, 255), 2)
        cv2.circle(image, center, 5, (0, 0, 255), -1)
        cv2.imshow("Frame", image)
        cv2.waitKey(0)
        return radius
    else:
        print "No ball found."
        exit(-1)


def distance_to_camera(knownWidth, focalLength, perWidth):
    # compute and return the distance from the marker to the camera
    return (knownWidth * focalLength) / perWidth

# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 24  # 12, 48 are the inches to blah 1 and blah 2

# initialize the known object width, which in this case, the piece of
# paper is 11 inches wide
KNOWN_RADIUS = 0.75

IMAGE_PATH = "C:\\Users\Max\\Pictures\\Camera Roll\\blah0.jpg"
TEST_IMAGE_PATHS = ["C:\\Users\\Max\\Pictures\\Camera Roll\\blah1.jpg", "C:\\Users\\Max\\Pictures\\Camera Roll\\blah3.jpg"]

# load the first image that contains an object that is KNOWN TO BE 2 feet
# from our camera, then find the marker in the image, and initialize
# the focal length
print "Reading image: " + IMAGE_PATH
image = cv2.imread(IMAGE_PATH)
marker_pixel_radius = find_marker_radius(image)
cv2.waitKey(0)
focalLength = (marker_pixel_radius * KNOWN_DISTANCE) / KNOWN_RADIUS
print "Focal length: " + str(focalLength)

# loop over the images
for imagePath in TEST_IMAGE_PATHS:
    # load the image, find the marker in the image, then compute the
    # distance to the marker from the camera
    image = cv2.imread(imagePath)
    marker_pixel_radius = find_marker_radius(image)
    inches = distance_to_camera(KNOWN_RADIUS, focalLength, marker_pixel_radius)

    print "Inches to object: " + str(inches)
    cv2.waitKey(0)

