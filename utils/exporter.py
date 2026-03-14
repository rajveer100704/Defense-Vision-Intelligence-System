from ultralytics import YOLO
from utils.logger import get_logger
import os

logger = get_logger()

def export_to_onnx(model_path="models/checkpoints/best.pt"):
    """
    Exports a trained YOLOv8 model to ONNX format for optimized inference.
    """
    if not os.path.exists(model_path):
        logger.error(f"Checkpoint not found at {model_path}. Using default yolov8n.pt")
        model_path = "yolov8n.pt"
        
    logger.info(f"Initializing Export: {model_path} -> ONNX")
    
    try:
        model = YOLO(model_path)
        # Export to ONNX
        path = model.export(format="onnx", int8=True, simplify=True)
        logger.info(f"Export successful. ONNX model saved at: {path}")
        return path
    except Exception as e:
        logger.error(f"Export failed: {e}")
        return None

if __name__ == "__main__":
    export_to_onnx()
