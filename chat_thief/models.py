from dataclasses import dataclass
from typing import List


@dataclass
class User:
    name: str
    permitted_commands: List


@dataclass
class CommandPermission:
    user: str
    command: str
    permitted_users: List[str]
    karma: int = 0


@dataclass
class SoundEffect:
    user: str
    youtube_id: str
    name: str
    start_time: str
    end_time: str
