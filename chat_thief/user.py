from chat_thief.models import _command_permissions_table, DEFAULT_DB_LOCATION

from tinydb import Query


class User:
    def __init__(self, name, db_location=DEFAULT_DB_LOCATION):
        self.name = name
        self.table = _command_permissions_table(db_location)

    def commands(self):
        def in_permitted_users(permitted_users, current_user):
            return current_user in permitted_users

        command_permissions = [
            permission["command"]
            for permission in self.table.search(
                Query().permitted_users.test(in_permitted_users, self.name)
            )
        ]
        return command_permissions
