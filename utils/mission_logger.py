import json
import os
import time
from datetime import datetime
from utils.logger import get_logger

logger = get_logger()

class MissionLogger:
    """
    Persists real-time surveillance events for historical replay and analysis.
    Stores data in newline-delimited JSON (JSONL) for efficient retrieval.
    """
    def __init__(self, mission_dir="logs/missions"):
        self.mission_dir = mission_dir
        os.makedirs(mission_dir, exist_ok=True)
        self.current_mission_file = None
        self.mission_id = None

    def start_mission(self):
        """
        Initializes a new mission log file.
        """
        self.mission_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mission_{self.mission_id}.jsonl"
        self.current_mission_file = os.path.join(self.mission_dir, filename)
        logger.info(f"Mission recording started: {self.current_mission_file}")
        
    def log_event(self, event_data):
        """
        Logs a single target event to the current mission file.
        """
        if not self.current_mission_file:
            self.start_mission()
            
        try:
            with open(self.current_mission_file, "a") as f:
                f.write(json.dumps(event_data) + "\n")
        except Exception as e:
            logger.error(f"Failed to log mission event: {e}")

    def list_missions(self):
        """
        Lists all recorded missions.
        """
        if not os.path.exists(self.mission_dir):
            return []
        
        files = [f for f in os.listdir(self.mission_dir) if f.endswith(".jsonl")]
        return sorted(files, reverse=True)

    def get_mission_events(self, filename):
        """
        Retrieves all events for a specific mission.
        """
        path = os.path.join(self.mission_dir, filename)
        if not os.path.exists(path):
            return []
            
        events = []
        with open(path, "r") as f:
            for line in f:
                events.append(json.loads(line))
        return events

mission_logger = MissionLogger()
