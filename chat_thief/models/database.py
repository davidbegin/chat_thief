from pathlib import Path

from tinydb.storages import MemoryStorage  # type: ignore
from tinydb import TinyDB  # type: ignore

from tinydb.table import Table


def db_table(db_location: Path, table_name: str) -> Table:
    return TinyDB(Path(__file__).parent.parent.parent.joinpath(db_location)).table(
        table_name, cache_size=0
    )
