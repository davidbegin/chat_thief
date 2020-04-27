import sys
import logging
from logging import FileHandler
from pathlib import Path


logger = logging.getLogger("Chat Log")
logger.setLevel(logging.INFO)
logs_path = Path(__file__).parent.parent.parent.joinpath("logs")
logs_path.mkdir(exist_ok=True)
logger.addHandler(FileHandler(logs_path.joinpath("chat.log")))
logger.addHandler(logging.StreamHandler(sys.stdout))
