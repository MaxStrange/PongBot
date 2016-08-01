"""
This module contains a script for finding a ping pong ball in a video and tracking its x, y, and z location.
"""

import imutils
import cv2

# Orange ball:
ORANGE_HSV_LOWER = (18, 69, 231)#(25, 0, 239)
ORANGE_HSV_UPPER = (42, 255, 255)#(36, 255, 255)

FOCAL_DISTANCE = 1861.83
BALL_RADIUS = 0.75

hsv_lower_range = ORANGE_HSV_LOWER
hsv_upper_range = ORANGE_HSV_UPPER

camera = cv2.VideoCapture()
opened = camera.open('POC\\pong2.mp4')

log = open("datalog.csv", 'wb')

if not opened:
    print "Failed to open the given video"
    exit(-1)

predicted_x = 0
predicted_y = 0
predicted_d = 0

last_x = 0
last_y = 0
last_d = 0

# Main loop
while True:
    # Get the next frame of video from the camera
    (grabbed, frame) = camera.read()

    if not grabbed:
        break

    # Resize the frame to be reasonable size
    frame = imutils.resize(frame, width=900)

    # Convert the image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # cv2.imshow("Frame", hsv)
    # cv2.waitKey(0)

    # Image processing pipeline
    mask = cv2.inRange(hsv, hsv_lower_range, hsv_upper_range)

    # cv2.imshow("Frame", mask)
    # cv2.waitKey(0)

    # mask = cv2.GaussianBlur(mask,(23, 23), 30)
    # cv2.imshow("Frame", mask)
    # cv2.waitKey(0)

    mask = cv2.erode(mask, None, iterations=2)

    # cv2.imshow("Frame", mask)
    # cv2.waitKey(0)

    mask = cv2.dilate(mask, None, iterations=2)

    # cv2.imshow("Frame", mask)
    # cv2.waitKey(0)

    # Find all the contours in the resultant image
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # If there are any contours in the image, there may be a ball in the image
    if len(cnts) > 0:
        # The biggest of the contours is most likely the ball
        ball_contour = max(cnts, key=cv2.contourArea)

        # Get the ball's min enclosing circle
        ((x, y), radius) = cv2.minEnclosingCircle(ball_contour)

        # Get the moments of the ball_contour
        M = cv2.moments(ball_contour)

        # Get the center of the ball as a tuple of x, y. This is also the x, y in our coordinate system
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        distance_from_camera = float(BALL_RADIUS * FOCAL_DISTANCE) / float(radius)

        # If the ball is big enough on the screen, draw a circle around it on the frame that displays on screen
        MIN_RADIUS = 2
        if radius > MIN_RADIUS:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 100, 100), 2)
            cv2.circle(frame, center, MIN_RADIUS, (0, 0, 255), -1)
            point_as_str = "(" + str(int(x)) + ", " + str(int(y)) + ", " + str(int(distance_from_camera)) + ")"
            cv2.putText(frame, point_as_str, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

            # Record the data
            xyz_data = "" + str(int(x)) + "," + str(int(y)) + "," + str(int(distance_from_camera)) + ","
            predicted_xyz_data = "" + str(int(predicted_x)) + "," + str(int(predicted_y)) + "," + str(int(predicted_d))
            data_point = xyz_data + predicted_xyz_data + "," + "\r\n"
            log.write(data_point)

        predicted_x = x + (x - last_x)
        predicted_y = y + (y - last_y)
        predicted_d = distance_from_camera + (distance_from_camera - last_d)

        last_x = x
        last_y = y
        last_d = distance_from_camera
    else:
        # No ball in this frame, move along
        pass

    # Display the resulting image in a frame on the screen
    cv2.imshow("Frame", frame)

    cv2.waitKey(0)

    # Wait for the user to push the q key to quit the program
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
            break

# Free the camera resource
camera.release()
log.close()