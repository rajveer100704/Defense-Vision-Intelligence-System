from tracking.track_pipeline import TrackingPipeline
from tracking.visualize_tracks import draw_tracks
from utils.logger import get_logger
import cv2
import os

logger = get_logger()

def verify_and_visualize():
    logger.info("Starting Tracking Visualization Verification...")
    
    sample_img_path = "datasets/dota/DOTAv1.5/images/P0000.jpg"
    if not os.path.exists(sample_img_path):
        logger.error(f"Sample image not found: {sample_img_path}")
        return

    pipeline = TrackingPipeline()
    
    # We'll process the same image twice to simulate a "video" of 2 static frames
    # This should at least trigger detections and basic tracking logic.
    
    output_dir = "runs/tracking"
    os.makedirs(output_dir, exist_ok=True)
    
    frame_count = 0
    # Custom loop to simulate frames
    for _ in range(2):
        frame = cv2.imread(sample_img_path)
        result = pipeline.tracker.detect_and_track(frame)
        pipeline.trajectory_manager.update(
            [type('Track', (), {'track_id': tid, 'xyxy': box}) 
             for tid, box in zip(result.boxes.id.cpu().numpy().astype(int), result.boxes.xyxy.cpu().numpy())]
            if result.boxes.id is not None else []
        )
        
        annotated_frame = draw_tracks(frame, result, pipeline.trajectory_manager.trajectories)
        
        out_path = os.path.join(output_dir, f"frame_{frame_count}.jpg")
        cv2.imwrite(out_path, annotated_frame)
        logger.info(f"Saved annotated frame to: {out_path}")
        frame_count += 1

    logger.info("Tracking visualization verification complete.")

if __name__ == "__main__":
    verify_and_visualize()
