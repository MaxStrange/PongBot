"""
A module to hold a class for tracking a ping pong ball.
"""

import cv2
import ball_state
import imutils


# Mishi:
MISH_HSV_LOWER = (0, 132, 82)
MISH_HSV_UPPER = (20, 255, 182)

# White ball:
WHITE_HSV_LOWER = (51, 0, 149)
WHITE_HSV_UPPER = (105, 57, 255)

# Orange ball:
ORANGE_HSV_LOWER = (18, 69, 231)#(25, 0, 239)
ORANGE_HSV_UPPER = (42, 255, 255)#(36, 255, 255)

FOCAL_DISTANCE = 1861.83
BALL_RADIUS = 0.75

hsv_lower_range = ORANGE_HSV_LOWER
hsv_upper_range = ORANGE_HSV_UPPER


class BallTracker:
    """
    A class for tracking a ping pong ball.
    """
    def __init__(self, frame):
        """
        Constructor.
        :param frame: The frame in which to find the ball.
        :return: void
        """
        self.__frame = frame
        self.__last_several_states = []
        self.__next_state = None

    def find_ball(self):
        """
        Uses the current image and finds a ball. Returns a BallState object.
        :return: A BallState object or None (if no ball found)
        """
        self.__frame = self.__image_pipeline()
        measured_ball_state = self.__measure_ball_position()

        if measured_ball_state:
            self.__next_state = self.__predict_next_state(measured_ball_state)
            self.__enqueue_state(measured_ball_state)
            return measured_ball_state
        else:
            return None

    def __calculate_averages(self):
        """
        Calculate the average x, y, and d velocities from the last several measurements.
        :return: A tuple: (average vx, average vy, average vd)
        """
        if not self.__last_several_states:
            return 0, 0, 0

        last_several_x = [state.get_x_velocity() for state in self.__last_several_states]
        last_several_y = [state.get_y_velocity() for state in self.__last_several_states]
        last_several_d = [state.get_d_velocity() for state in self.__last_several_states]

        average = lambda seq: sum(seq) / len(seq)
        avg_x = average(last_several_x)
        avg_y = average(last_several_y)
        avg_d = average(last_several_d)

        return avg_x, avg_y, avg_d

    def __calculate_velocities(self, current_state):
        """
        Calculates the ball's velocity values in x, y, and d directions
        :param current_state: The current state of the ball
        :return:
        """
        if self.get_last_state():
            print "Last X: " + str(self.get_last_state().get_x_pos()) + " Y: " + str(self.get_last_state().get_y_velocity())
            print "This X: " + str(current_state.get_x_pos()) + " Y: " + str(current_state.get_y_pos())
            vx = current_state.get_x_pos() - self.get_last_state().get_x_pos()
            vy = current_state.get_y_pos() - self.get_last_state().get_y_pos()
            vd = current_state.get_d_pos() - self.get_last_state().get_d_pos()
            return vx, vy, vd
        else:
            return 0, 0, 0

    def __constrain_to_average(self, measured_velocities, avgs):
        """
        Moves the measured velocities towards the given averages.
        :param measured_velocities:
        :param avgs: A tuple of averages of the form (vxavg, vyavg, vdavg)
        :return: A new tuple of velocities which is closer to the average
        """
        constrain = lambda i: ((0.6 * measured_velocities[i]) + (0.4 * avgs[i]))
        return constrain(0), constrain(1), constrain(2)

    def __enqueue_state(self, ball_state):
        """
        Enqueue the state into the list of last several states to help track the ball in the future.
        :param ball_state: The state to enqueue
        :return: void
        """
        self.__last_several_states.append(ball_state)
        if len(self.__last_several_states) > 3:
            self.__last_several_states.pop(0)

    def __image_pipeline(self):
        """
        Takes an image and processes it to a resultant image that should have the ball
        as a white blob and with everything else black.
        :return: The image after processing
        """
        # Convert the image to HSV
        hsv = cv2.cvtColor(self.__frame, cv2.COLOR_BGR2HSV)

        # Convert everything non-orange into black and everything orange into white
        in_ranged = cv2.inRange(hsv, hsv_lower_range, hsv_upper_range)
        # cv2.imshow("inranged", in_ranged)
        # cv2.waitKey(0)

        # If estimate of ball's position is good enough, take that region of the image out before eroding and
        # put it back in afterwards.
        roi = None
        if self.get_predicted_state():
            likely_x, likely_y, likely_rad = self.get_predicted_state().get_x_pos(), \
                                             self.get_predicted_state().get_y_pos(), \
                                             self.get_predicted_state().get_d_pos()
            x_range_left = likely_x - (likely_rad * 5)
            x_range_right = likely_x + (likely_rad * 5)
            y_range_up = likely_y - (likely_rad * 5)
            y_range_down = likely_y + (likely_rad * 5)
            # TODO: Get this working
            roi = in_ranged[y_range_up:y_range_down, x_range_left:x_range_right]

        # Erode resultant white blobs a bit to destroy noise and to cut down on competing white blobs
        eroded = cv2.erode(in_ranged, None, iterations=2)

        # cv2.imshow("eroded", eroded)
        # cv2.waitKey(0)

        if roi is not None:
            eroded[y_range_up:y_range_down, x_range_left:x_range_right] = roi

        # Dilate the eroded stuff back to normal - but the noise will still be gone
        dilated = cv2.dilate(eroded, None, iterations=2)

        # cv2.imshow("dilated", dilated)
        # cv2.waitKey(0)

        return dilated

    def __measure_ball_position(self):
        """
        Measures the ball's position from the image, if it can find the ball in the image. Otherwise returns None.
        :return: a BallState object or None if not found
        """
        contours = cv2.findContours(self.__frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        center = None

        # If there are any contours in the image, there may be a ball in the image
        if contours:
            # The biggest of the contours is most likely the ball
            ball_contour = max(contours, key=cv2.contourArea)

            # Get the ball's min enclosing circle and x, y location in pixels
            ((x, y), radius) = cv2.minEnclosingCircle(ball_contour)

            # Get the moments of the ball_contour
            M = cv2.moments(ball_contour)

            # Get the center of the ball as a tuple of x, y. This is also the x, y in our coordinate system
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # Get a more accurate guess at the radius before using it for distance calculation
            if self.get_last_state():
                # If the radius is suddenly much smaller than last time, it is likely an incomplete ball detection,
                # in which case, we should use the last ball radius for our distance calculation
                last_radius = self.get_last_state().get_radius()
                min_radius = (0.5 * last_radius) if (last_radius < 30) else (0.25 * last_radius)
                radius = last_radius if radius < min_radius else radius

            distance_from_camera = float(BALL_RADIUS * FOCAL_DISTANCE) / float(radius)

            return ball_state.BallState(x, y, distance_from_camera, radius=radius)
        else:
            # No ball in this frame
            return None

    def __predict_next_state(self, current_state):
        """
        Predicts the next measurements of the ball and returns it
        :param current_state:
        :return: BallState object
        """
        # Calculate the ball's velocities in x, y, and d
        measured_velocities = self.__calculate_velocities(current_state)

        print "Vel0: " + str(measured_velocities[0]) + ", " + str(measured_velocities[1])

        avgs = self.__calculate_averages()
        measured_velocities = self.__constrain_to_average(measured_velocities, avgs)

        print "Vel1: " + str(measured_velocities[0]) + ", " + str(measured_velocities[1])

        # Side-effect: Also update this state with the newly calculated velocities
        current_state.set_x_velocity(measured_velocities[0])
        current_state.set_y_velocity(measured_velocities[1])
        current_state.set_d_velocity(measured_velocities[2])

        # Predict what the next time step's values will be using measured_velocities
        predicted_x = current_state.get_x_pos() + measured_velocities[0]
        predicted_y = current_state.get_y_pos() + measured_velocities[1]
        predicted_d = current_state.get_d_pos() + measured_velocities[2]

        next_state = ball_state.BallState(predicted_x, predicted_y, predicted_d, measured_velocities[0],
                                          measured_velocities[1], measured_velocities[2], current_state.get_radius())
        return next_state

    def get_last_state(self):
        """
        Gets the last measured state of the ball
        :return: the last measured state of the ball
        """
        if self.__last_several_states:
            return self.__last_several_states[-1]
        else:
            return None

    def get_predicted_state(self):
        """
        Gets the state that is predicted for the next time frame
        :return: the next state
        """
        return self.__next_state

    def set_frame(self, frame):
        """
        Sets the frame that this object acts on
        :param frame:
        :return: void
        """
        self.__frame = frame
