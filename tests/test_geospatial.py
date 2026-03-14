import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from geospatial.geo_mapper import GeoMapper
from geospatial.coordinate_transform import get_bbox_center
from geospatial.map_visualizer import MapVisualizer
from utils.logger import get_logger

logger = get_logger()

def test_geospatial_pipeline():
    logger.info("Starting Geospatial Pipeline Verification Test...")
    
    # 1. Initialize Mapper (Try real file if exists)
    tif_path = "datasets/spacenet/AOI_2_Vegas/image.tif"
    if os.path.exists(tif_path):
        mapper = GeoMapper(tif_path)
    else:
        logger.warning(f"Real imagery not found at {tif_path}, using mock mapper.")
        mapper = GeoMapper()
    
    # 2. Simulate detection
    bbox = [100, 100, 200, 200]
    cx, cy = get_bbox_center(bbox)
    logger.info(f"Bbox center: ({cx}, {cy})")
    
    # 3. Convert to Geo
    lat, lon = mapper.pixel_to_geo(cx, cy)
    logger.info(f"Geographic Coordinates: Lat {lat:.6f}, Lon {lon:.6f}")
    
    # 4. Visualize on Map
    visualizer = MapVisualizer()
    visualizer.add_target(lat, lon, target_id=101, cls_name="test_asset", confidence=0.95)
    
    output_map = "tests/test_tactical_map.html"
    visualizer.save(output_map)
    
    if os.path.exists(output_map):
        logger.info(f"Geospatial verification successful. Map saved to {output_map}")
    else:
        logger.error("Geospatial verification failed: Map not saved.")

if __name__ == "__main__":
    test_geospatial_pipeline()
