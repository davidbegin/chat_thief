from logging import FileHandler
from pathlib import Path
import logging
import sys


def setup_logger():
    logger = logging.getLogger("Test Logs")
    logs_path = Path(__file__).parent.parent.parent.joinpath("tmp")
    logs_path.mkdir(exist_ok=True)
    logger.addHandler(FileHandler(logs_path.joinpath("chat.log")))
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger
