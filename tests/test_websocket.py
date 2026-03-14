import asyncio
import websockets
import json
import time

async def test_ws():
    uri = "ws://localhost:8000/ws"
    print(f"Connecting to {uri}...")
    try:
        async with websockets.connect(uri) as websocket:
            print("Connected. Sending mock target...")
            mock_target = {
                "id": 99,
                "class": "test-drone",
                "lat": 36.1627,
                "lon": -115.1391,
                "confidence": 0.98
            }
            await websocket.send(json.dumps(mock_target))
            print("Message sent. Waiting for broadcast echo (if implemented)...")
            # In our app, manager.broadcast(data) sends it to ALL clients.
            # We are a client, so we might receive it back.
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"Received broadcast: {response}")
            except asyncio.TimeoutError:
                print("No broadcast received (expected if server logic differs).")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_ws())
