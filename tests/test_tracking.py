import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tracking.track_pipeline import TrackingPipeline
from utils.logger import get_logger

logger = get_logger()

def test_tracking():
    logger.info("Starting Tracking Verification Test...")
    
    # Check if we have a sample image to treat as a frame
    sample_img = "datasets/dota/DOTAv1.5/images/P0000.jpg"
    if not os.path.exists(sample_img):
        logger.error(f"Sample image not found: {sample_img}")
        return

    pipeline = TrackingPipeline()
    results = pipeline.run_on_video(sample_img)
    
    if results:
        logger.info("Tracking test successful (inference stage verified)")
        # Check if any IDs were assigned
        valid_tracks = any(r.boxes.id is not None for r in results)
        if valid_tracks:
            logger.info("Target IDs successfully assigned.")
        else:
            logger.warning("No Target IDs assigned (Single frame or no detections). This is expected for a static image track test.")
    else:
        logger.error("Tracking test failed to return results.")

if __name__ == "__main__":
    test_tracking()
