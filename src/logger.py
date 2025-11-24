import logging
import os
from datetime import datetime

# Create logs directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Create log file name using timestamp
LOG_FILE = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Logging format
LOG_FORMAT = (
    "[%(asctime)s] — %(levelname)s — "
    "[%(module)s:%(lineno)d] — %(message)s"
)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format=LOG_FORMAT,
    level=logging.INFO,
)

def get_logger():
    """
    Returns a logger instance.
    Use this when you need a logger for a specific module.
    """
    logger = logging.getLogger()
    return logger
