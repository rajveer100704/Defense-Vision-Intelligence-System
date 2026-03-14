import sys
import os
import time
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tracking.predictor import MotionPredictor
from utils.logger import get_logger

logger = get_logger()

def test_prediction_accuracy():
    logger.info("Starting Motion Prediction Verification Test...")
    
    predictor = MotionPredictor(dt=1.0)
    track_id = 7
    
    # Simulate a target moving in a straight line
    # Velocity: +10 units/step in X and Y
    path = [(0, 0), (10, 10), (20, 20), (30, 30), (40, 40)]
    
    logger.info("Feeding linear trajectory to Kalman Filter...")
    for i, pos in enumerate(path):
        est_pos = predictor.update(track_id, pos)
        logger.info(f"Step {i}: Observed {pos} -> Estimated {est_pos}")

    # Predict future position (5 steps ahead)
    # Expected: 40 + (5 * 10) = 90
    prediction = predictor.predict_future(track_id, steps=5)
    logger.info(f"Prediction for +5 steps: {prediction}")
    
    expected = [90., 90.]
    error = np.linalg.norm(np.array(prediction) - np.array(expected))
    
    if error < 5.0:
        logger.info(f"Prediction accuracy verified. Error: {error:.4f}")
    else:
        logger.error(f"Prediction error too high: {error:.4f}. Expected around {expected}")

if __name__ == "__main__":
    test_prediction_accuracy()
