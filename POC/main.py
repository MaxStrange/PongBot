"""
This module contains a script for finding a ping pong ball and tracking its x, y, and z location.
"""

import cv2
from ball_tracking import ball_tracker, ball_state
from data_recorder import data_recorder
from ui import frame_drawer
import imutils


USE_LIVE_VIDEO = False
PATH_TO_VIDEO = "pong2.mp4"


def cleanup(camera, log_file):
    """
    Cleans up the resources used by the program.
    :param camera: The open camera reference to close.
    :param log_file: The log file to close.
    :return: void
    """
    camera.release()
    log_file.close()


def run_loop(camera, log_file):
    """
    Runs the main application logic. Runs through the video (or webcam grab). Finds the ball, measures its current
    distance, and predicts what the next location of the ball will be. Logs the data.
    :param camera: An open reference to a video or webcam.
    :param log_file: The file to log data in.
    :return: void
    """
    # Initialize classes to use throughout loop
    drawer = frame_drawer.FrameDrawer(None)
    tracker = ball_tracker.BallTracker(None)
    recorder = data_recorder.DataRecorder(log_file)

    # Run the loop
    while True:
        # Get the next frame of video from the camera, or else we are done
        grabbed, frame = camera.read()
        if not grabbed:
            break
        else:
            frame = imutils.resize(frame, width=900)
            drawer.set_frame(frame)
            tracker.set_frame(frame)

        predicted_state = tracker.get_predicted_state()

        # Find the ball and get its location and info from the image
        measured_ball_state = tracker.find_ball()

        # Draw a frame but don't show it yet
        drawer.paint_prediction_box(predicted_state)
        drawer.circle_ball_and_show(measured_ball_state)

        if predicted_state and measured_ball_state:
            print "Predicted: " + predicted_state.to_str(as_int=True)
            print "Measured: " + measured_ball_state.to_str(as_int=True)

        if measured_ball_state:
            # Record the data
            recorder.record_data(measured_ball_state.get_x_pos(), measured_ball_state.get_y_pos(),
                                 measured_ball_state.get_d_pos(), tracker.get_predicted_state().get_x_pos(),
                                 tracker.get_predicted_state().get_y_pos(), tracker.get_predicted_state().get_d_pos())

        # Wait for the user to push the q key to quit the program or any button to move to next frame
        if USE_LIVE_VIDEO:
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
    if USE_LIVE_VIDEO:
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture()
        camera.open(PATH_TO_VIDEO)

    log_file = open('datalogFORPONG2.csv', 'w')
    return camera, log_file


if __name__ == '__main__':
    camera, log_file = setup()
    run_loop(camera, log_file)
    cleanup(camera, log_file)
