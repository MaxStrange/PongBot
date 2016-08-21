"""
This module contains a script for finding a ping pong ball and tracking its x, y location and distance from camera.
"""

import cv2
from ball_tracking import ball_tracker, ball_state
from data_recorder import data_recorder
from ui import frame_drawer
import imutils
import config
import kalman.control as kf
import socket


def cleanup(camera, log_file, soc):
    """
    Cleans up the resources used by the program.
    :param camera: The open camera reference to close.
    :param log_file: The log file to close.
    :param soc: TCP socket
    :return: void
    """
    camera.release()
    log_file.close()
    if soc:
        soc.close()


def run_loop(camera, log_file, soc):
    """
    Runs the main application logic. Runs through the video (or webcam grab). Finds the ball, measures its current
    distance, and predicts what the next location of the ball will be. Logs the data.
    :param camera: An open reference to a video or webcam.
    :param log_file: The file to log data in.
    :param soc: TCP socket
    :return: void
    """
    # Initialize classes to use throughout loop
    drawer = frame_drawer.FrameDrawer(None)
    tracker = ball_tracker.BallTracker(None)
    recorder = data_recorder.DataRecorder(log_file)
    kf.initialize(kf.package_state_as_vector(0, 0, 0, 0, 0, 0))

    # Run the loop
    while True:
        # Get the next frame of video from the camera, or else we are done
        grabbed, frame = camera.read()
        if not grabbed:
            break
        else:
            frame = imutils.resize(frame, width=config.IMAGE_WIDTH, height=config.IMAGE_HEIGHT)
            drawer.set_frame(frame)
            tracker.set_frame(frame)

        predicted_state = tracker.get_predicted_state()

        # Find the ball and get its location and info from the image
        measured_ball_state = tracker.find_ball()
        updated_prediction = tracker.get_predicted_state()

        # Draw a frame but don't show it yet
        drawer.paint_prediction_box(predicted_state)
        drawer.circle_ball_and_show(measured_ball_state)

        if predicted_state and measured_ball_state:
            print "Predicted: " + predicted_state.to_str(as_int=True)
            print "Measured: " + measured_ball_state.to_str(as_int=True)

        # Code below makes a Kalman filter that works, but seems to add slightly more noise rather than damp the noise
        # In all truth, I'm not sure that even tuning it perfectly would be worth the amount of computation, as it
        # is already pretty good at predicting the next state of the ball.
        # if measured_ball_state:
        #     # Filter the data using a Kalman Filter and update the ball_tracker with the newly found data
        #     state_vector = kf.package_state_as_vector(measured_ball_state.get_x_pos(),
        #                                               measured_ball_state.get_y_pos(),
        #                                               measured_ball_state.get_d_pos(),
        #                                               measured_ball_state.get_x_velocity(),
        #                                               measured_ball_state.get_y_velocity(),
        #                                               measured_ball_state.get_d_velocity())
        #     kf.update(state_vector)
        #     updated_vector = kf.get_filtered_state()
        #     updated_ball_state = ball_state.BallState(*kf.unpack_state(updated_vector))
        #     updated_ball_state.set_radius(measured_ball_state.get_radius())
        #     measured_ball_state = updated_ball_state
        #     tracker.set_current_state(measured_ball_state)

        if measured_ball_state:
            # Record the data
            recorder.record_data(measured_ball_state.get_x_pos(), measured_ball_state.get_y_pos(),
                                 measured_ball_state.get_d_pos(), tracker.get_predicted_state().get_x_pos(),
                                 tracker.get_predicted_state().get_y_pos(), tracker.get_predicted_state().get_d_pos())
            formatted_state = measured_ball_state.format_for_sending()
            if soc:
                soc.send(formatted_state)

        # Wait for the user to push the q key to quit the program or any button to move to next frame
        if config.USE_LIVE_VIDEO:
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                    break
        else:
            cv2.waitKey(0)

def setup():
    """
    Initializes the camera and the datalog file and returns them.
    :return: A tuple: Opened camera, opened file.
    """
    if config.USE_LIVE_VIDEO:
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture()
        camera.open(config.PATH_TO_VIDEO)

    log_file = open('datalogFORPONG2.csv', 'w')

    soc = None
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((config.TCP_IP, config.TCP_PORT))
    except socket.error as e:
        print str(e)
        print "Socket will be unnavailable."
        soc = None

    return camera, log_file, soc


if __name__ == '__main__':
    camera, log_file, soc = setup()
    run_loop(camera, log_file, soc)
    cleanup(camera, log_file, soc)
