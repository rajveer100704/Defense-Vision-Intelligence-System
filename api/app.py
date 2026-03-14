from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from api.websocket_manager import manager
from utils.mission_logger import mission_logger
from utils.logger import get_logger
import os
import json
import asyncio

logger = get_logger()

app = FastAPI(title="Defense Vision Intelligence System")

# Active Node Registry
active_nodes = set()

# Serve dashboard static files
dashboard_path = os.path.join(os.getcwd(), "dashboard")
if os.path.exists(dashboard_path):
    app.mount("/dashboard", StaticFiles(directory=dashboard_path), name="dashboard")

@app.get("/health")
def health():
    return {
        "status": "ok", 
        "system": "Defense Vision Intelligence",
        "active_nodes": list(active_nodes)
    }

@app.post("/ingest")
async def ingest_event(event: dict):
    """
    Ingest target events and persist to mission logs.
    """
    node_id = event.get("node", "unknown-node")
    active_nodes.add(node_id)
    
    # Persist to Mission Log
    mission_logger.log_event(event)
    
    # Broadcast to dashboard
    await manager.broadcast(json.dumps(event))
    return {"status": "ingested", "node": node_id}

@app.get("/missions/list")
def list_missions():
    return {"missions": mission_logger.list_missions()}

@app.get("/missions/replay/{filename}")
async def replay_mission(filename: str):
    """
    Streams historical mission events back to the dashboard.
    """
    events = mission_logger.get_mission_events(filename)
    if not events:
        return {"status": "error", "message": "Mission not found"}
        
    logger.info(f"Replaying mission {filename} via dashboard...")
    
    async def stream_replay():
        for event in events:
            # Add a 'replay' flag for UI distinction
            event["is_replay"] = True
            await manager.broadcast(json.dumps(event))
            # Simulate real-time delay (e.g., 100ms between frames)
            await asyncio.sleep(0.1)
            
    # Run replay in background to not block the request
    asyncio.create_task(stream_replay())
    return {"status": "started", "events_queued": len(events)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Receive data (e.g. status updates from dashboard)
            data = await websocket.receive_text()
            # For now, we mainly use ws for broadcasting, 
            # but we can echo back or handle commands here.
            logger.debug(f"Received from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Defense Intelligence API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
