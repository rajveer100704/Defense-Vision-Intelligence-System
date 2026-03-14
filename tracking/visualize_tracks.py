import cv2
import numpy as np
from pathlib import Path
from utils.logger import get_logger

logger = get_logger()

def draw_tracks(frame, result, trajectories=None):
    """
    Draw bounding boxes, IDs, and trajectory lines on the frame.
    result: YOLOv8 Result object
    trajectories: dict of ID -> list of center points
    """
    if result.boxes.id is None:
        return frame

    boxes = result.boxes.xyxy.cpu().numpy()
    ids = result.boxes.id.cpu().numpy().astype(int)
    clss = result.boxes.cls.cpu().numpy().astype(int)
    names = result.names

    for box, track_id, cls in zip(boxes, ids, clss):
        x1, y1, x2, y2 = map(int, box)
        label = f"{names[cls]} ID:{track_id}"
        
        # Draw box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw trajectory tail
        if trajectories and track_id in trajectories:
            points = trajectories[track_id]
            if len(points) > 1:
                # Draw lines between consecutive points
                for i in range(1, len(points)):
                    cv2.line(frame, points[i-1], points[i], (0, 255, 255), 2)
                
    return frame

if __name__ == "__main__":
    logger.info("Visualize tracks module ready.")
