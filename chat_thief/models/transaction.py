from tinydb import TinyDB, Query  # type: ignore
from tinydb.table import Table  # type: ignore
from tinydb.storages import MemoryStorage  # type: ignore
import contextlib


class AbortTransaction(Exception):
    pass


def abort():
    raise AbortTransaction


@contextlib.contextmanager
def transaction(table: Table):
    tables = table.storage.read()
    if tables is None:
        tables = {}

    data = tables.get(table.name, {})
    data = {table.document_id_class(id): doc for id, doc in data.items()}
    db = TinyDB(storage=MemoryStorage)

    tmp_table = db.table(table.name)
    tmp_table.storage.write(tables)

    try:
        yield tmp_table

        tables[table.name] = tmp_table.storage.read()[table.name]
        table.storage.write(tables)
        table._next_id = None

    except AbortTransaction:
        pass
