from dataclasses import dataclass
from typing import List


@dataclass
class CommandPermission:
    user: str
    command: str
    permitted_users: List[str]
    health: int = 5
