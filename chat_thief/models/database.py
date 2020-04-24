from pathlib import Path

from tinydb import TinyDB, Query

USERS_DB_PATH = "db/users.json"
COMMANDS_DB_PATH = "db/commands.json"


def db_table(db_location, table_name):
    return TinyDB(Path(__file__).parent.parent.parent.joinpath(db_location)).table(table_name)
