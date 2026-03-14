from ultralytics import YOLO, settings
import os
import yaml
from utils.logger import get_logger

logger = get_logger()

# Disable external loggers that might cause URI issues on Windows
settings.update({'mlflow': False, 'wandb': False, 'clearml': False, 'comet': False})

class YOLOPipeline:
    def __init__(self, model_name="yolov8n.pt"):
        logger.info(f"Initializing YOLO pipeline with model: {model_name}")
        self.model = YOLO(model_name)

    def train(self, data_config, epochs=1, batch=8, imgsz=320): # Smaller imgsz/batch for smoke test
        logger.info(f"Starting training on {data_config} for {epochs} epochs...")
        # device='cpu' and workers=0 are more stable for smoke tests on some Windows environments
        results = self.model.train(
            data=data_config,
            epochs=epochs,
            batch=batch,
            imgsz=imgsz,
            device='cpu',
            workers=0,
            project="runs/detect",
            name="train_dota",
            exist_ok=True,
            plots=True,
            save=True
        )
        logger.info("Training complete.")
        return results

    def infer(self, image_path):
        logger.info(f"Running inference on: {image_path}")
        results = self.model(image_path)
        return results

if __name__ == "__main__":
    pipeline = YOLOPipeline()
    # Smoke test with 1 epoch
    pipeline.train("datasets/dota/dota.yaml", epochs=1)
