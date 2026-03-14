import numpy as np
from ultralytics import YOLO
from utils.logger import get_logger

logger = get_logger()
# In YOLOv8, trackers are often used via model.track, 
# but for manual control we can access the underlying class or logic.
# However, to keep it simple and robust on Windows, we'll implement a wrapper
# that utilizes the ultralytics tracking logic but maintains our own state.

class Tracker:
    def __init__(self, model_path="yolov8n.pt"):
        logger.info(f"Initializing Tracker with model: {model_path}")
        self.detector = YOLO(model_path)
        # We'll use the model's built-in tracking capabilities but expose 
        # a manual-like interface for the pipeline to stay standard.
        # This ensures we don't break on complex internal imports.

    def detect_and_track(self, frame, persist=True):
        """
        Detection + Tracking in one pass (optimized).
        Returns results containing track IDs.
        """
        results = self.detector.track(
            source=frame,
            persist=persist,
            tracker="bytetrack.yaml",
            conf=0.3,
            iou=0.5,
            verbose=False
        )
        return results[0] # Return the first result object
