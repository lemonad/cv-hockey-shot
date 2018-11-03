"""
Kalman filtering for 2d point (fixed timesteps).

"""
from datetime import datetime

import cv2
import numpy as np

HISTORY_SIZE = 9
STATE_SIZE = 4
MEASURE_SIZE = 2
CONTROL_SIZE = 0


class KalmanPoint:
    def __init__(self, timestep, process_noise_cov=None, measurement_noise_cov=None):
        if process_noise_cov is None:
            process_noise_cov = np.array([1e-1, 1e-1, 1e-1, 1e-1], "float32")
        if measurement_noise_cov is None:
            measurement_noise_cov = np.array([1e-1, 1e-1], "float32")

        self.kf = cv2.KalmanFilter(STATE_SIZE, MEASURE_SIZE, CONTROL_SIZE)
        self.state = np.zeros(STATE_SIZE, "float32")  # [x, y, vx, vy]
        self.meas = np.zeros(MEASURE_SIZE, "float32")  # [zx, zy]

        # State transition matrix (A).
        # Used for calculating (and updating) the estimated, or next, state of the
        # parameters. It is updated with dt in the predict phase which results in the
        # following transitions:

        # position_i (x, y) = position_{i-1} + dt_i * velocity_{i-1}
        # velocity_i (vx, vy) = velocity_{i-1}

        # In matrix form:

        # [ 1  0  dt 0  ]
        # [ 0  1  0  dt ]
        # [ 0  0  1  0  ]
        # [ 0  0  0  1  ]
        self.kf.transitionMatrix = np.zeros((STATE_SIZE, STATE_SIZE), "float32")
        cv2.setIdentity(self.kf.transitionMatrix)
        self.kf.transitionMatrix[0, 2] = timestep
        self.kf.transitionMatrix[1, 3] = timestep

        # Face detections results in two sensor measurements, position (x, y). I.e.
        #   [ 1 0 0 0 ]
        #   [ 0 1 0 0 ]
        #   [ 0 0 0 0 ]
        #   [ 0 0 0 0 ]
        self.kf.measurementMatrix = np.zeros((MEASURE_SIZE, STATE_SIZE), "float32")
        self.kf.measurementMatrix[0, 0] = 1.0
        self.kf.measurementMatrix[1, 1] = 1.0

        # Process Noise Covariance Matrix (Q):
        #   [ Ex  0   0   0   ]
        #   [ 0   Ey  0   0   ]
        #   [ 0   0   Evx 0   ]
        #   [ 0   0   0   Evy ]
        self.kf.processNoiseCov = np.zeros((STATE_SIZE, STATE_SIZE), "float32")
        self.kf.processNoiseCov[0, 0] = process_noise_cov[0]
        self.kf.processNoiseCov[1, 1] = process_noise_cov[1]
        self.kf.processNoiseCov[2, 2] = process_noise_cov[2]
        self.kf.processNoiseCov[3, 3] = process_noise_cov[3]

        # Measurement Noise Covariance Matrix (R).
        #   [ Ex 0  ]
        #   [ 0  Ey ]
        # Since we are using pixels, magnitudes will be around one.
        self.kf.measurementNoiseCov = np.zeros((MEASURE_SIZE, MEASURE_SIZE), "float32")
        self.kf.measurementNoiseCov[0, 0] = measurement_noise_cov[0]
        self.kf.measurementNoiseCov[1, 1] = measurement_noise_cov[1]

        # Error Covariance
        self.kf.errorCovPre = np.zeros((STATE_SIZE, STATE_SIZE), "float32")
        self.kf.errorCovPre[0, 0] = 1.0
        self.kf.errorCovPre[1, 1] = 1.0
        self.kf.errorCovPre[2, 2] = 1.0
        self.kf.errorCovPre[3, 3] = 1.0

        self.kf.statePost = np.zeros((STATE_SIZE, 1), "float32")
        self.found = False

    def predict(self):
        predPoint = np.zeros(2)

        # Have previous detections?
        if self.found:
            self.state = self.kf.predict()

            predPoint[0] = self.state[0]
            predPoint[1] = self.state[1]
        return predPoint

    def restart(self):
        self.found = False

    def correct(self, point):
        self.meas[0] = point[0]
        self.meas[1] = point[1]

        if self.found:
            self.kf.correct(self.meas)
        else:
            self.kf.errorCovPre[0, 0] = 1.0
            self.kf.errorCovPre[1, 1] = 1.0
            self.kf.errorCovPre[2, 2] = 1.0
            self.kf.errorCovPre[3, 3] = 1.0

            self.state[0] = self.meas[0]
            self.state[1] = self.meas[1]
            self.state[2] = 0.0
            self.state[3] = 0.0

            self.kf.statePost = self.state
            self.found = True
