import sys
import logging
from logging import FileHandler
from pathlib import Path


logger = logging.getLogger("Chat Log")
logger.setLevel(logging.INFO)
logs_path = Path(__file__).parent.parent.parent.joinpath("logs")
logs_path.mkdir(exist_ok=True)
logger.addHandler(FileHandler(logs_path.joinpath("chat.log")))

SUCCESS = "\033[92m"
WARNING = "\033[94m"
ERROR = "\033[91m"
CLEAR = "\033[0m"


def success(msg: str) -> None:
    print(f"{SUCCESS}{msg}{CLEAR}")


def warning(msg: str) -> None:
    print(f"{WARNING}{msg}{CLEAR}")


def error(msg: str) -> None:
    print(f"{ERROR}{msg}{CLEAR}")
