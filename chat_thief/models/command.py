from chat_thief.models.database import db_table


class Command:
    table_name = "commands"
    database_folder = ""
    database_path = "db/commands.json"

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def count(cls):
        return len(cls.db().all())
