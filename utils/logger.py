from loguru import logger
import sys
from pathlib import Path

# Ensure the log directory is created relative to the script's location or use absolute if preferred
# Here we use Path("logs") assuming the CWD is the project root
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True, parents=True)

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

logger.add(
    LOG_DIR / "system.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO"
)

def get_logger():
    return logger
