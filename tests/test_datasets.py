import sys
import os

# Add the project root to sys.path to allow relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datasets.download_datasets import main as download
from datasets.dataset_validator import validate_dataset
from utils.logger import get_logger

logger = get_logger()

def test_pipeline():
    logger.info("Starting Dataset Pipeline Test...")

    # For testing purposes, we might want to skip actual huge downloads if they are landing pages
    # or just let it try once.
    try:
        logger.info("Triggering download process...")
        download()
    except Exception as e:
        logger.error(f"Download process failed: {e}")

    logger.info("Validating datasets directory...")
    validate_dataset("datasets")

if __name__ == "__main__":
    test_pipeline()
