import numpy as np
from filterpy.kalman import KalmanFilter
from utils.logger import get_logger

logger = get_logger()

class MotionPredictor:
    """
    Uses a Kalman Filter (Constant Velocity Model) to predict future target positions.
    """
    def __init__(self, dt=1.0):
        self.dt = dt
        self.filters = {} # track_id -> KalmanFilter

    def _init_filter(self, initial_pos):
        """
        Initialize a new Kalman Filter for a target.
        State vector x: [pos_x, pos_y, vel_x, vel_y]
        """
        kf = KalmanFilter(dim_x=4, dim_z=2)
        kf.x = np.array([initial_pos[0], initial_pos[1], 0., 0.])
        
        # State transition matrix
        kf.F = np.array([[1., 0., self.dt, 0.],
                         [0., 1., 0., self.dt],
                         [0., 0., 1., 0.],
                         [0., 0., 0., 1.]])
        
        # Measurement matrix (we only measure position)
        kf.H = np.array([[1., 0., 0., 0.],
                         [0., 1., 0., 0.]])
        
        # Covariance matrix
        kf.P *= 10.
        kf.R *= 5. # Measurement noise
        kf.Q = np.eye(4) * 0.1 # Process noise
        
        return kf

    def update(self, track_id, current_pos):
        if track_id not in self.filters:
            self.filters[track_id] = self._init_filter(current_pos)
            return current_pos

        kf = self.filters[track_id]
        kf.predict()
        kf.update(current_pos)
        return kf.x[:2]

    def predict_future(self, track_id, steps=5):
        """
        Predict position 'steps' into the future.
        """
        if track_id not in self.filters:
            return None

        kf = self.filters[track_id]
        # Copy current state
        future_x = kf.x.copy()
        
        # Project state forward
        for _ in range(steps):
            future_x = np.dot(kf.F, future_x)
            
        return future_x[:2]

    def cleanup(self, active_ids):
        """
        Remove filters for tracks that are no longer active.
        """
        dead_ids = [tid for tid in self.filters if tid not in active_ids]
        for tid in dead_ids:
            del self.filters[tid]
            logger.debug(f"Cleaned up Kalman Filter for dead ID: {tid}")
