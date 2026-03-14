from utils.logger import get_logger

logger = get_logger()

class ThreatEngine:
    """
    Elite Adaptive Threat Scoring Engine.
    Calculates threat levels based on target type, kinematics, and spatial context.
    """
    def __init__(self, restricted_zones=None):
        self.restricted_zones = restricted_zones or []
        # Weights for threat calculation
        self.weights = {
            "type": 0.4,
            "velocity": 0.3,
            "proximity": 0.2,
            "anomaly": 0.1
        }
        # Base weights for different object classes
        self.class_threat_base = {
            "airplane": 0.8,
            "helicopter": 0.9,
            "truck": 0.6,
            "car": 0.3,
            "ship": 0.7,
            "bus": 0.4
        }
        logger.info("Elite ThreatEngine initialized.")

    def calculate_score(self, target_data):
        """
        Calculates a normalized threat score (0.0 to 1.0).
        target_data: {id, class, lat, lon, velocity, trajectory_len, restricted_zones_dist}
        """
        score = 0.0
        
        # 1. Type Score
        cls_name = target_data.get("class", "unknown").lower()
        type_score = self.class_threat_base.get(cls_name, 0.5)
        score += type_score * self.weights["type"]

        # 2. Velocity Score (Normalizing around 50 m/s for this prototype)
        velocity = target_data.get("velocity", 0.0)
        vel_score = min(velocity / 50.0, 1.0)
        score += vel_score * self.weights["velocity"]

        # 3. Proximity Score (Distance to nearest restricted zone)
        dist_to_zone = target_data.get("dist_to_zone", 1000.0) # Assume far if unknown
        # Normalize: threat is high if dist is low. (Close = 1.0 threat)
        prox_score = max(0, 1.0 - (dist_to_zone / 500.0)) 
        score += prox_score * self.weights["proximity"]

        # 4. Anomaly/Behavior Score (e.g. loitering)
        # For now, simple trajectory length vs displacement heuristic
        anomaly_score = 0.0
        if target_data.get("is_loitering"):
            anomaly_score = 1.0
        score += anomaly_score * self.weights["anomaly"]

        return round(score, 3)

    def get_threat_level(self, score):
        if score > 0.8: return "CRITICAL"
        if score > 0.6: return "HIGH"
        if score > 0.4: return "MEDIUM"
        return "LOW"

    def check_target(self, target):
        score = self.calculate_score(target)
        level = self.get_threat_level(score)
        
        return {
            "score": score,
            "level": level,
            "factors": {
                "velocity": target.get("velocity"),
                "dist_to_zone": target.get("dist_to_zone"),
                "is_loitering": target.get("is_loitering")
            }
        }
