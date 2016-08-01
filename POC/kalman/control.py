"""
This module takes in measurements and gives out the next time step's
predicted measurements for the ball position.
"""

import numpy

from POC.kalman import mykalman

# Constants for this particular application

# At 30 frames per second, deltaT should be 1/30 seconds
_DEL_T = 0.03333333

# A is the matrix that occurs in real life due to the change from one
# timestep to the next in the real state. It is the matrix that
# Wikipedia calls F. It gets multiplied by the state vector.
_KALMAN_A = numpy.matrix([
                            [1, _DEL_T, 0, 0, 0, 0],
                            [0, 1,      0, 0, 0, 0],
                            [0, 0, 1, _DEL_T, 0, 0],
                            [0, 0, 0, 1,      0, 0],
                            [0, 0, 0, 0, 1, _DEL_T],
                            [0, 0, 0, 0, 0, 1]
                          ])
# _KALMAN_A = numpy.matrix([1])

# B is the matrix which is responsible for mapping the control vector
# into the same space as the state vector and then adding to it.
# Wikipedia also calls this matrix B.
_KALMAN_B = numpy.matrix([
                            [0],
                            [0],
                            [0.5 * _DEL_T * _DEL_T],
                            [_DEL_T],
                            [0],
                            [0]
                          ])
# _KALMAN_B = numpy.matrix([0])

# The control vector is usually a vector. But in this case, we are using
# a scalar, as it should work fine either way.
#_CONTROL = -9.8  # m/s^2 TODO: Should be in pix/s^2 - the fov is shallow enough that this should be invariant throughout it
_CONTROL = 0

# H is the matrix which moves the measured state into the same space as the
# actual state. It should usually(?) just be an identity matrix.
_KALMAN_H = numpy.matrix([
                            [1, 0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0, 1]
                          ])
# _KALMAN_H = numpy.matrix([1])

# Q is the process error matrix. TODO: I don't know what this is.
_KALMAN_Q = numpy.matrix([
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0]
                          ])
# _KALMAN_Q = numpy.matrix([0])

# R is the measurement error covariance matrix. This has to be tweaked.
_KALMAN_R = numpy.matrix([
                            [0.00001, 0, 0, 0, 0, 0],
                            [0, 0.00001, 0, 0, 0, 0],
                            [0, 0, 0.1, 0, 0, 0],
                            [0, 0, 0, 0.002, 0, 0],
                            [0, 0, 0, 0, 0.002, 0],
                            [0, 0, 0, 0, 0, 0.1]
                          ])
# _KALMAN_R = numpy.matrix([0.2])

_filter = None


def package_state_as_vector(x, vx, y, vy, d, vd):
    """
    Packages the state into a single numpy state vector.
    Use this vector for updating and initializing.
    :param x: The x location of the ball in pixels
    :param vx: The measured x velocity of the ball in pixels/sec
    :param y: The y location of the ball in pixels
    :param vy: The measured y velocity of the ball in pixels/sec
    :param d: The measured distance from the camera in inches
    :param vd: The measured d velocity of the ball in pixels/sec
    :return: a state vector
    """
    return numpy.matrix([
                            [x],
                            [vx],
                            [y],
                            [vy],
                            [d],
                            [vd]
                         ])


def unpack_state(state_vector):
    """
    Unpacks a state vector into a tuple of x, vx, y, vy, d, vd.
    :param state_vector: The state vector to unpack.
    :return: A tuple of x, vx, y, vy, d, vd
    """
    x = state_vector[0, 0]
    vx = state_vector[1, 0]
    y = state_vector[2, 0]
    vy = state_vector[3, 0]
    d = state_vector[4, 0]
    vd = state_vector[5, 0]
    return x, vx, y, vy, d, vd


def initialize(state_vector):
    """
    Initialize the Kalman filter with your best guess as to the state.
    :param state_vector: The best guess as to the initial state.
    :return: void
    """
    # our initial guess at the covariance of the state is identity
    P = numpy.matrix([
                        [1, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1]
                      ])
    # P = numpy.matrix([1])
    global _filter
    _filter = mykalman.MyKalmanFilter(_KALMAN_A, _KALMAN_B, _KALMAN_H, state_vector, P, _KALMAN_Q, _KALMAN_R)
    

def update(measured_state):
    """
    Updates the Kalman filter with the given measured state.
    The Kalman filter will have an estimate of what the next state will
    be given this measurement and what it has collected so far.
    :param measured_state: The state vector that you measured.
    :return: void
    """
    _filter.update(_CONTROL, measured_state)


def get_filtered_state():
    """
    Gets the state after it has gone through the Kalman Filter.
    :return: A state vector that is the updated state
    """
    return _filter.get_current_state()
