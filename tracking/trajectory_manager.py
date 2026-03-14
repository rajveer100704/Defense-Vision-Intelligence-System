from utils.logger import get_logger
from tracking.predictor import MotionPredictor

logger = get_logger()

class TrajectoryManager:
    """
    Manages historical positions of tracked objects.
    Enables motion analysis, velocity estimation, and behavioral modeling.
    """
    def __init__(self, max_points=100):
        self.trajectories = {} # ID -> list of (x, y) coordinates
        self.max_points = max_points
        self.predictor = MotionPredictor()
        logger.info(f"TrajectoryManager initialized with max_points={max_points} and Predictive Intelligence enabled.")

    def update(self, tracks):
        """
        Update trajectories with new track positions.
        'tracks' should be a list of track objects with 'track_id' and 'tlwh' (top, left, width, height).
        """
        for track in tracks:
            # Note: Depending on the tracker implementation, attributes might vary.
            # We assume track has .track_id and .tlwh or similar.
            track_id = getattr(track, 'track_id', None)
            if track_id is None:
                continue

            # Get center point
            if hasattr(track, 'tlwh'):
                x, y, w, h = track.tlwh
                center = (int(x + w / 2), int(y + h / 2))
            elif hasattr(track, 'xyxy'): # fallback for different formats
                x1, y1, x2, y2 = track.xyxy
                center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
            else:
                continue

            if track_id not in self.trajectories:
                self.trajectories[track_id] = []
                logger.debug(f"New trajectory started for ID: {track_id}")

            self.trajectories[track_id].append(center)
            
            # Update Kalman Filter for prediction
            self.predictor.update(track_id, center)

            # Keep only the last max_points
            if len(self.trajectories[track_id]) > self.max_points:
                self.trajectories[track_id].pop(0)

    def get_trajectory(self, track_id):
        return self.trajectories.get(track_id, [])

    def get_prediction(self, track_id, steps=5):
        """
        Get predicted future position for a track.
        """
        return self.predictor.predict_future(track_id, steps)

    def clear_dead_tracks(self, active_ids):
        """
        Optionally clear memory for tracks no longer active.
        """
        dead_ids = [tid for tid in self.trajectories if tid not in active_ids]
        for tid in dead_ids:
            # In a real system, we might save this to a database before deleting
            # For now, just remove to save memory
            del self.trajectories[tid]
            self.predictor.cleanup(active_ids) # Propagate cleanup
            logger.debug(f"Cleared trajectory for dead ID: {tid}")
