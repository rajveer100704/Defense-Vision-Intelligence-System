import cv2
from tracking.tracker import Tracker
from tracking.trajectory_manager import TrajectoryManager
from tracking.visualize_tracks import draw_tracks
from geospatial.geo_mapper import GeoMapper
from pipelines.threat_engine import ThreatEngine
from models.behavior_lstm import TrajectoryForecaster
from utils.logger import get_logger
from pathlib import Path
import time
import numpy as np

logger = get_logger()

class TrackingPipeline:
    def __init__(self, model_path="yolov8n.pt", geo_image_path=None):
        self.tracker = Tracker(model_path)
        self.trajectory_manager = TrajectoryManager()
        self.geo_mapper = GeoMapper(geo_image_path) if geo_image_path else GeoMapper(mock_mode=True)
        self.threat_engine = ThreatEngine()
        self.forecaster = TrajectoryForecaster()
        logger.info("TrackingPipeline initialized with full GEOINT and Behavioral AI stack.")

    def process_video(self, video_path, output_path=None):
        logger.info(f"Processing video: {video_path}")
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error(f"Could not open video: {video_path}")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Detection + Tracking
            result = self.tracker.detect_and_track(frame)
            
            # Extract tracks for TrajectoryManager
            tracks = []
            if result.boxes.id is not None:
                boxes = result.boxes.xyxy.cpu().numpy()
                ids = result.boxes.id.cpu().numpy().astype(int)
                for box, track_id in zip(boxes, ids):
                    # Create a simple box object for the manager
                    # In a real scenario, this would be a Track object
                    tracks.append(type('Track', (), {'track_id': track_id, 'xyxy': box}))

            # Update trajectories
            self.trajectory_manager.update(tracks)
            
            # Elite Processing: Geospatial + Behavioral
            processed_data = []
            active_ids = []
            
            if result.boxes.id is not None:
                ids = result.boxes.id.cpu().numpy().astype(int)
                boxes = result.boxes.xyxy.cpu().numpy()
                confs = result.boxes.conf.cpu().numpy()
                classes = result.boxes.cls.cpu().numpy()
                names = result.names

                for i, track_id in enumerate(ids):
                    active_ids.append(track_id)
                    x1, y1, x2, y2 = boxes[i]
                    center_px = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                    
                    # 1. Pixel -> Geo
                    lat, lon = self.geo_mapper.pixel_to_geo(center_px[0], center_px[1])
                    
                    # 2. Short-term Prediction (Kalman)
                    pred_px = self.trajectory_manager.get_prediction(track_id)
                    pred_lat, pred_lon = (None, None)
                    if pred_px:
                        pred_lat, pred_lon = self.geo_mapper.pixel_to_geo(int(pred_px[0]), int(pred_px[1]))
                    
                    # 3. Long-term Prediction (LSTM)
                    traj = self.trajectory_manager.get_trajectory(track_id)
                    lt_path_px = self.forecaster.predict_multi_step(traj)
                    lt_path_geo = []
                    for ppx in lt_path_px:
                        glat, glon = self.geo_mapper.pixel_to_geo(int(ppx[0]), int(ppx[1]))
                        lt_path_geo.append([glat, glon])
                    
                    # 4. Threat Scoring
                    # Calculate simple velocity for threat engine
                    velocity = 0.0
                    if len(traj) > 1:
                        p1, p2 = traj[-2], traj[-1]
                        velocity = np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2) # px/frame

                    threat_info = self.threat_engine.check_target({
                        "id": track_id,
                        "class": names[int(classes[i])],
                        "lat": lat, "lon": lon,
                        "velocity": velocity,
                        "dist_to_zone": 1000.0, # Placeholder until zone integration
                        "is_loitering": False   # Placeholder
                    })

                    processed_data.append({
                        "id": track_id,
                        "class": names[int(classes[i])],
                        "lat": lat, "lon": lon,
                        "predicted_lat": pred_lat,
                        "predicted_lon": pred_lon,
                        "long_term_path": lt_path_geo,
                        "threat_score": threat_info["score"],
                        "threat_level": threat_info["level"],
                        "confidence": confs[i],
                        "timestamp": time.time()
                    })

            self.trajectory_manager.clear_dead_tracks(active_ids)
            yield frame, processed_data

        cap.release()
        logger.info(f"Video processing complete: {video_path}")

if __name__ == "__main__":
    pipeline = TrackingPipeline()
    # Mock test on image
    for frame, result in pipeline.process_video("datasets/dota/DOTAv1.5/images/P0000.jpg"):
        if result.boxes.id is not None:
            logger.info(f"Tracked IDs: {result.boxes.id}")
