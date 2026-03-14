from utils.logger import get_logger
import os

logger = get_logger()

try:
    import folium
    FOLIUM_AVAILABLE = True
except ImportError:
    logger.warning("folium not found. MapVisualizer will run in mock mode.")
    FOLIUM_AVAILABLE = False

class MapVisualizer:
    """
    Generates interactive maps with plotted tactical targets.
    """
    def __init__(self, center_lat=36.1627, center_lon=-115.1391, zoom=13):
        self.center = [center_lat, center_lon]
        self.zoom = zoom
        self.map = None
        
        if FOLIUM_AVAILABLE:
            self.map = folium.Map(location=self.center, zoom_start=self.zoom, tiles='OpenStreetMap')
        
    def add_target(self, lat, lon, target_id, cls_name, confidence=None):
        if not self.map:
            logger.warning(f"Map not initialized. Target {target_id} at {lat}, {lon} logged but not plotted.")
            return

        popup_text = f"ID: {target_id} | {cls_name}"
        if confidence:
            popup_text += f"<br>Conf: {confidence:.2f}"
            
        folium.Marker(
            [lat, lon],
            popup=popup_text,
            tooltip=f"{cls_name} ({target_id})",
            icon=folium.Icon(color='red')
        ).add_to(self.map)

    def save(self, output_path="dashboard/tactical_map.html"):
        if self.map:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            self.map.save(output_path)
            logger.info(f"Tactical map saved to {output_path}")
        else:
            logger.error("Cannot save map: Folium not available or map not initialized.")
