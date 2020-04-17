from tinydb import Query

from chat_thief.database import db_table, USERS_DB_PATH, COMMANDS_DB_PATH


class User:
    def __init__(
        self, name, users_db_path=USERS_DB_PATH, commands_db_path=COMMANDS_DB_PATH
    ):
        self.name = name
        self.users_db = db_table(users_db_path, "users")
        self.commands_db = db_table(commands_db_path, "commands")

    def commands(self):
        def in_permitted_users(permitted_users, current_user):
            return current_user in permitted_users

        command_permissions = [
            permission["command"]
            for permission in self.commands_db.search(
                Query().permitted_users.test(in_permitted_users, self.name)
            )
        ]
        return command_permissions

    def doc(self):
        pass
