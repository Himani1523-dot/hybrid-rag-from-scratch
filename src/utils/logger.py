"""logger.py"""
import logging
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = os.path.join(
    LOG_DIR,
    f"rag_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)

def setup_logger():
    root_logger = logging.getLogger()

    if root_logger.handlers:
        return  # prevent duplicate logs

    root_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)