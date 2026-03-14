import requests
import json
import time
from utils.logger import get_logger

logger = get_logger()

class NodeAgent:
    """
    Distributed Node Agent that sends tracking events to a central command server.
    """
    def __init__(self, node_id, server_url="http://localhost:8000"):
        self.node_id = node_id
        self.server_url = server_url
        self.session = requests.Session()
        logger.info(f"Node Agent {node_id} initialized. Targeted server: {server_url}")

    def publish_event(self, target_event):
        """
        Sends a target event to the central server.
        """
        # Add node metadata
        target_event["node"] = self.node_id
        
        try:
            # We'll use a standard POST endpoint for ingestion to keep it simple,
            # but this could be a WebSocket client in a high-throughput system.
            response = self.session.post(
                f"{self.server_url}/ingest",
                json=target_event,
                timeout=1.0
            )
            if response.status_code != 200:
                logger.error(f"Node {self.node_id} failed to ingest: {response.status_code}")
        except Exception as e:
            logger.error(f"Node {self.node_id} connection error: {e}")

    def stream_mock_data(self, base_lat=36.1627, base_lon=-115.1391, count=5):
        """
        Simulate a stream of targets for testing.
        """
        logger.info(f"Node {self.node_id} starting mock data stream...")
        for i in range(count):
            event = {
                "id": i + (hash(self.node_id) % 100),
                "class": "mock-uav",
                "lat": base_lat + (i * 0.001),
                "lon": base_lon + (i * 0.001),
                "threat_level": "LOW",
                "confidence": 0.95,
                "timestamp": time.time()
            }
            self.publish_event(event)
            time.sleep(0.5)
