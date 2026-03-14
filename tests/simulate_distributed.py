import asyncio
import os
import sys
import threading
from distributed.node_agent import NodeAgent
from utils.logger import get_logger

# Ensure project root in path
sys.path.append(os.getcwd())

logger = get_logger()

def start_node(node_id, lat_offset, lon_offset):
    agent = NodeAgent(node_id)
    # Simulate a stream of targets with spatial offsets
    agent.stream_mock_data(
        base_lat=36.1627 + lat_offset, 
        base_lon=-115.1391 + lon_offset, 
        count=10
    )

if __name__ == "__main__":
    logger.info("Starting Multi-Node Surveillance Simulation...")
    
    # Simulate 3 Nodes: Drone Alpha, Drone Beta, Satellite Gamma
    nodes = [
        ("DRONE_ALPHA", 0.005, 0.005),
        ("DRONE_BETA", -0.005, -0.005),
        ("SATELLITE_GAMMA", 0.010, -0.010)
    ]
    
    threads = []
    for node_id, lat_off, lon_off in nodes:
        t = threading.Thread(target=start_node, args=(node_id, lat_off, lon_off))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
        
    logger.info("Distributed Simulation Complete.")
