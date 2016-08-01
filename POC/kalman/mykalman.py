"""
Implementation of a Linear Kalman Filter class.
"""

import numpy


class MyKalmanFilter:
    """
    Implementation of a Linear Kalman Filter.
    Feed it the initial values and invariants, and then everytime you
    get another measurement from sensors, call update on it.
    After that, it will have the next time step's predicted state.
    """
    def __init__(self, _A, _B, _H, _x, _P, _Q, _R):
        """
        Constructor.
        @param _A: The transformation matrix for the state of the system
        @param _B: The transformation matrix for the control of the system
        @param _H: The transformation matrix for the measurement of the system
        @param _x: The current state of the system
        @param _P: The covariance matrix
        @param _Q: The process error matrix
        @param _R: The measurement error covariance matrix
        """
        self.A = _A
        self.B = _B
        self.H = _H
        self.current_state_estimate = _x
        self.current_prob_estimate = _P
        self.Q = _Q
        self.R = _R

    def get_current_state(self):
        """
        Gets the current state of the system as predicted by the Kalman filter.
        @return: The current state of the system (x - a state vector).
        """
        return self.current_state_estimate

    def update(self, control_vector, measurement_vector):
        """
        Takes the next vector of control state and the next measurement vector and
        updates the current state to predict the next one.
        @param control_vector: The next vector of control state
        @param measurement_vector: The next measurement vector
        @return: void
        """
        # Prediction step
        predicted_state_estimate = self.A * self.current_state_estimate + self.B * control_vector
        predicted_prob_estimate = (self.A * self.current_prob_estimate) * numpy.transpose(self.A) + self.Q

        # Observation step
        innovation = measurement_vector - self.H * predicted_state_estimate
        innovation_covariance = self.H * predicted_prob_estimate * numpy.transpose(self.H) + self.R
        
        # Update step
        kalman_gain = predicted_prob_estimate * numpy.transpose(self.H) * numpy.linalg.inv(innovation_covariance)
        self.current_state_estimate = predicted_state_estimate + kalman_gain * innovation
        size_of_prob_est_matrix = self.current_prob_estimate.shape[0]
        self.current_prob_estimate = (numpy.eye(size_of_prob_est_matrix) - kalman_gain * self.H) * predicted_prob_estimate
