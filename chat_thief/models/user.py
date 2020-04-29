from tinydb import Query

from chat_thief.models.database import db_table, USERS_DB_PATH, COMMANDS_DB_PATH
from chat_thief.prize_dropper import random_soundeffect
from chat_thief.soundeffects_library import SoundeffectsLibrary

from chat_thief.models.command import Command


class User:
    # I want to pass in class configuration
    def __init__(
        self, name, users_db_path=USERS_DB_PATH, commands_db_path=COMMANDS_DB_PATH
    ):
        self.name = name
        self.users_db = db_table(users_db_path, "users")
        self.commands_db = db_table(commands_db_path, "commands")

    def total_users(self):
        return len(self.users_db.all())

    def total_street_cred(self):
        users = self.users_db.all()
        return sum([user["street_cred"] for user in users])

    def total_cool_points(self):
        users = self.users_db.all()
        return sum([user["cool_points"] for user in users])

    def purge(self):
        return self.users_db.purge()

    def stats(self):
        return f"@{self.name} - Street Cred: {self.street_cred()} | Cool Points: {self.cool_points()}"

    def paperup(self, amount=100):
        self.add_street_cred(amount)
        self.add_cool_points(amount)
        return f"{self.name} has been Papered Up"

    # This doesn't iterate properly
    # the early returns will break multiple purchases
    def buy(self, effect):
        if self.cool_points() > 0:
            # We should remove the random thang into the class
            if effect == "random":
                looking_for_effect = True
                while looking_for_effect:
                    effect = random_soundeffect()

                    if not Command(effect).allowed_to_play(self.name):
                        looking_for_effect = False
                        self.remove_cool_points()

                        Command(effect).allow_user(self.name)
                        return f"@{self.name} purchased: {effect}"
            else:
                if Command(effect).allowed_to_play(self.name):
                    return f"@{self.name} already has access to !{effect}"
                else:
                    self.remove_cool_points()
                    Command(effect).allow_user(self.name)
        else:
            return f"@{self.name} - Out of Cool Points to Purchase with"

        return f"@{self.name} purchased: !{effect}"

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
        return {
            "name": self.name,
            "street_cred": 0,
            "cool_points": 0,
        }

    def _find_or_create_user(self):
        user_result = self.users_db.search(Query().name == self.name)
        if user_result:
            print(f"WE GOT A USER: {user_result}")
            user_result = user_result[0]
            return user_result
        else:
            print(f"Creating New User: {self.doc()}")
            from tinyrecord import transaction

            with transaction(self.users_db) as tr:
                tr.insert(self.doc())
            return self.doc()

    def street_cred(self):
        user = self._find_or_create_user()
        return user["street_cred"]

    def cool_points(self):
        user = self._find_or_create_user()
        return user["cool_points"]

    def remove_cool_points(self):
        user = self._find_or_create_user()

        def decrease_cred():
            def transform(doc):
                doc["cool_points"] = doc["cool_points"] - 1

            return transform

        self.users_db.update(decrease_cred(), Query().name == self.name)

    def add_cool_points(self, amount=1):
        user = self._find_or_create_user()

        def increase_cred():
            def transform(doc):
                doc["cool_points"] = doc["cool_points"] + amount

            return transform

        self.users_db.update(increase_cred(), Query().name == self.name)

    def remove_street_cred(self, amount=1):
        user = self._find_or_create_user()

        def decrease_cred():
            def transform(doc):
                doc["street_cred"] = doc["street_cred"] - amount

            return transform

        self.users_db.update(decrease_cred(), Query().name == self.name)

    def add_street_cred(self, amount=1):
        user = self._find_or_create_user()

        def increase_cred():
            def transform(doc):
                doc["street_cred"] = doc["street_cred"] + amount

            return transform

        self.users_db.update(increase_cred(), Query().name == self.name)

    def remove_all_commands(self):
        user = self._find_or_create_user()

        def _remove_all_commands(user):
            def transform(doc):
                new_users = list(set(doc["permitted_users"]) - set(user))
                doc["permitted_users"] = new_users

            return transform

        # how do I put something on a new line
        # without going to insert
        for command in self.commands():
            self.commands_db.update(
                _remove_all_commands(user), Query().command == command
            )
