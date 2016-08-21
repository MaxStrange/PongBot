"""
The configuration parameters for this program.
Tune these to your specifications.
"""

# If True, will use the webcam on the computer. If False, will use PATH_TO_VIDEO
USE_LIVE_VIDEO = False
PATH_TO_VIDEO = "pong2.mp4"

# HSV values for a white ball:
WHITE_HSV_LOWER = (51, 0, 149)
WHITE_HSV_UPPER = (105, 57, 255)

# HSV values for an orange ball:
ORANGE_HSV_LOWER = (18, 69, 231)
ORANGE_HSV_UPPER = (42, 255, 255)

# The focal distance for this camera as measured using the 'script_and_stuff/distance_to_object.py' script
FOCAL_DISTANCE = 1861.83

# The radius of the ping pong ball in inches
BALL_RADIUS = 0.75

# The pixel width of the image after you resize it - then it gets processed at that size
IMAGE_WIDTH = 900
IMAGE_HEIGHT = 900

# The actual hsv values that the ball_tracker will use
hsv_lower_range = ORANGE_HSV_LOWER
hsv_upper_range = ORANGE_HSV_UPPER

# Top left point for the rectangle that will be the portion of the image we process
TOP_LEFT = (int(IMAGE_WIDTH / 3), 0)

# Bottom right point for the rectangle that will be the portion of the image we process
BOTTOM_RIGHT = (int(IMAGE_WIDTH * 4.5 / 3), IMAGE_HEIGHT)

# TCP stuff
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
