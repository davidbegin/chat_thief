from dataclasses import dataclass
from typing import List
from pathlib import Path


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
