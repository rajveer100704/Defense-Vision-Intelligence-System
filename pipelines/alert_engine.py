from utils.logger import get_logger

logger = get_logger()

class AlertEngine:
    """
    Tactical alert engine to monitor target behavior and spatial constraints.
    """
    def __init__(self):
        # Example: Restricted zones defined by Lat/Long bounds
        self.restricted_zones = [
            {
                "id": "ZONE_ALPHA",
                "lat_min": 36.160, "lat_max": 36.165,
                "lon_min": -115.145, "lon_max": -115.135,
                "description": "High Security Sector Alpha"
            }
        ]

    def check_alert(self, target):
        """
        Check if a target triggers any tactical alerts.
        """
        lat = target.get("lat")
        lon = target.get("lon")
        
        if lat is None or lon is None:
            return None

        for zone in self.restricted_zones:
            if zone["lat_min"] < lat < zone["lat_max"] and \
               zone["lon_min"] < lon < zone["lon_max"]:
                alert = {
                    "type": "RESTRICTED_ZONE_INCURSION",
                    "level": "CRITICAL",
                    "zone_id": zone["id"],
                    "description": zone["description"],
                    "target_id": target["id"]
                }
                logger.warning(f"ALERT: {alert['type']} for Target {target['id']} in {zone['id']}")
                return alert
        
        return None
