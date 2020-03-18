import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


logger = logging.getLogger("Chat Log")
logger.setLevel(logging.INFO)
logs_path = Path(__file__).parent.parent.joinpath("logs")
logs_path.mkdir(exist_ok=True)
# Figure out the actual values we want and make them configurable
logger.addHandler(
    RotatingFileHandler(
        logs_path.joinpath("chat.log"), maxBytes=50000000, backupCount=5
    )
)
logger.addHandler(logging.StreamHandler(sys.stdout))
