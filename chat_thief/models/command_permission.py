from dataclasses import dataclass
from typing import List
# from pathlib import Path


@dataclass
class CommandPermission:
    user: str
    command: str
    permitted_users: List[str]
    karma: int = 0
