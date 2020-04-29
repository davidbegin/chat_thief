from dataclasses import dataclass
from pathlib import Path
from typing import List

from tinydb import TinyDB, Query

from chat_thief.models.database import db_table

COMMANDS_DB_PATH = "db/commands.json"


@dataclass
class CommandPermission:
    # This is moving beyong a simple dataclass
    user: str
    command: str
    permitted_users: List[str]
    health: int = 5

    database_path = COMMANDS_DB_PATH
    table_name = "commands"
    db = db_table(database_path, table_name)

    def is_healthy(self):
        return self.database_path
        # return True

# def commands_table():
#     return db_table(COMMANDS_DB_PATH)

# def db_table(db_location, table_name):
#     return TinyDB(Path(__file__).parent.parent.parent.joinpath(db_location)).table(table_name, cache_size=0)

