from dataclasses import dataclass
from typing import List
from pathlib import Path

TABLE_NAME = "command_permissions"
DEFAULT_DB_LOCATION = "db/soundeffects.json"

from tinydb import TinyDB, Query


def _command_permissions_table(db_location):
    soundeffects_db_path = Path(__file__).parent.parent.joinpath(db_location)
    return TinyDB(soundeffects_db_path).table(TABLE_NAME)


# @dataclass
# class User:
#     name: str
#     permitted_commands: List


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
