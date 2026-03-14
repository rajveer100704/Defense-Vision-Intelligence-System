from utils.logger import get_logger
import os

logger = get_logger()

try:
    import rasterio
    from pyproj import Transformer
    RASTERIO_PROJ_AVAILABLE = True
except ImportError:
    logger.warning("rasterio or pyproj not found. GeoMapper will run in mock mode.")
    RASTERIO_PROJ_AVAILABLE = False

class GeoMapper:
    """
    Handles conversion between pixel coordinates and geographic coordinates (Lat/Long).
    Supports CRS transformation from projected coordinates to WGS84.
    """
    def __init__(self, image_path=None):
        self.image_path = image_path
        self.dataset = None
        self.transform = None
        self.transformer = None
        
        if image_path and RASTERIO_PROJ_AVAILABLE:
            try:
                self.dataset = rasterio.open(image_path)
                self.transform = self.dataset.transform
                self.crs = self.dataset.crs
                
                # Initialize transformer to WGS84 (EPSG:4326)
                self.transformer = Transformer.from_crs(
                    self.crs,
                    "EPSG:4326",
                    always_xy=True
                )
                logger.info(f"Loaded geospatial metadata from {image_path} (CRS: {self.crs})")
            except Exception as e:
                logger.error(f"Failed to open {image_path}: {e}")
        elif not RASTERIO_PROJ_AVAILABLE:
            logger.warning("Running in geospatial mock mode.")

    def pixel_to_geo(self, x, y):
        """
        Converts pixel (x, y) to (latitude, longitude).
        """
        if self.transform and self.transformer:
            # 1. Pixel -> Projected Coordinates (e.g. UTM)
            projected_x, projected_y = self.transform * (x, y)
            # 2. Projected -> WGS84 (Lon, Lat)
            lon, lat = self.transformer.transform(projected_x, projected_y)
            return lat, lon
        else:
            # Mock conversion for demonstration (centered around a sample AOI)
            base_lat, base_lon = 36.1627, -115.1391
            lat = base_lat + (y * 0.00001)
            lon = base_lon + (x * 0.00001)
            return lat, lon

    def close(self):
        if self.dataset:
            self.dataset.close()
