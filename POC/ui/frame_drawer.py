"""
A module for holding a class for drawing the frame.
"""

import cv2
import imutils
from ball_tracking import ball_state


class FrameDrawer:
    """
    A class for drawing the frame.
    """
    def __init__(self, frame):
        """
        Constructor
        :param frame: The image to manipulate
        :return: void
        """
        self.__frame = frame

    def circle_ball_and_show(self, ball_state_to_draw):
        """
        Circles the ball in the frame if it exists. Otherwise just shows the frame.
        :param ball_state_to_draw: The state of the ball that you want to draw in the frame
        :return: void
        """
        MIN_RADIUS = 2

        if ball_state_to_draw:
            x = ball_state_to_draw.get_x_pos()
            y = ball_state_to_draw.get_y_pos()
            d = ball_state_to_draw.get_d_pos()
            radius = ball_state_to_draw.get_radius()

            if radius > MIN_RADIUS:
                cv2.circle(self.__frame, (int(x), int(y)), int(radius), (0, 100, 100), 2)
                cv2.circle(self.__frame, (int(x), int(y)), MIN_RADIUS, (0, 0, 255), -1)
                point_as_str = "(" + str(int(x)) + ", " + str(int(y)) + ", " + str(int(d)) + ")"
                cv2.putText(self.__frame, point_as_str, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

        # Either way, show the image
        cv2.imshow("Frame", self.__frame)

    def paint_prediction_box(self, predicted_state):
        """
        Paints a box around where the program believed the ball would be this time
        :param predicted_state: The state we are predicting
        :return: void
        """
        if not predicted_state:
            return

        point_one = (int(predicted_state.get_x_pos() - (predicted_state.get_radius() * 2)),
                     (int(predicted_state.get_y_pos() - (predicted_state.get_radius() * 2))))
        point_two = (int((predicted_state.get_x_pos() + (predicted_state.get_radius() * 2))),
                     (int(predicted_state.get_y_pos() + (predicted_state.get_radius() * 2))))
        cv2.circle(self.__frame, point_one, 5, (0, 255, 0), 5)
        cv2.circle(self.__frame, point_two, 5, (255, 0, 0), 5)
        cv2.circle(self.__frame, (int(predicted_state.get_x_pos()), int(predicted_state.get_y_pos())), 5, (0, 0, 0), 5)
        color = (255, 0, 255)
        thickness = 5
        cv2.rectangle(self.__frame, point_one, point_two, color, thickness)

    def resize(self, width):
        """
        Resizes the frame drawer's frame to the given width
        :param width:
        :return: The resized frame
        """
        # Resize the frame to be reasonable size
        self.__frame = imutils.resize(self.__frame, width=900)

    def set_frame(self, frame):
        """
        Sets the image that this object manipulates
        :param frame: The image
        :return: void
        """
        self.__frame = frame