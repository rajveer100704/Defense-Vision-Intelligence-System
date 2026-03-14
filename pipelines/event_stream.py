import json

def create_target_event(track_data):
    """
    Serializes target state for WebSocket transmission.
    track_data: dict containing id, class, lat, lon, etc.
    """
    event = {
        "id": track_data.get("id"),
        "class": track_data.get("class", "unknown"),
        "lat": track_data.get("lat"),
        "lon": track_data.get("lon"),
        "predicted_lat": track_data.get("predicted_lat"),
        "predicted_lon": track_data.get("predicted_lon"),
        "threat_score": track_data.get("threat_score", 0.0),
        "threat_level": track_data.get("threat_level", "LOW"),
        "long_term_path": track_data.get("long_term_path", []),
        "confidence": round(track_data.get("confidence", 0.0), 2),
        "timestamp": track_data.get("timestamp")
    }
    return json.dumps(event)
