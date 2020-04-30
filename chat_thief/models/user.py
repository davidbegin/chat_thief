from tinydb import Query

from chat_thief.models.database import db_table, USERS_DB_PATH, COMMANDS_DB_PATH
from chat_thief.prize_dropper import random_soundeffect
from chat_thief.soundeffects_library import SoundeffectsLibrary

from chat_thief.models.command import Command


class User:
    table_name = "users"
    database_folder = ""
    database_path = "db/users.json"

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def count(cls):
        return len(cls.db().all())

    def __init__(self, name):
        self.name = name

    def total_users(self):
        return len(self.db().all())

    def total_street_cred(self):
        users = self.db().all()
        return sum([user["street_cred"] for user in users])

    def total_cool_points(self):
        users = self.db().all()
        return sum([user["cool_points"] for user in users])

    def purge(self):
        return self.db().purge()

    def stats(self):
        return f"@{self.name} - Street Cred: {self.street_cred()} | Cool Points: {self.cool_points()}"

    def paperup(self, amount=100):
        self.add_street_cred(amount)
        self.add_cool_points(amount)
        return f"{self.name} has been Papered Up"

    def _find_affordable_random_command(self, cost):
        looking_for_effect = True

        while looking_for_effect:
            # Should we update this query to take cost parameter?
            effect = random_soundeffect()
            # We need to check the cost
            command = Command(effect)
            if self.cool_points >= command.cost() and not command.allowed_to_play(
                self.name
            ):
                looking_for_effect = False
        return command

    def buy(self, effect):
        if self.cool_points() > 0:
            if effect == "random":
                command = self._find_affordable_random_command()
                self.remove_cool_points(command.cost())
                command.allow_user(self.name)
                command.increase_cost()
                return f"@{self.name} purchased: {command.name}"
            else:
                if Command(effect).allowed_to_play(self.name):
                    return f"@{self.name} already has access to !{effect}"
                else:
                    command = Command(effect)

                    if self.cool_points() >= command.cost():
                        self.remove_cool_points(command.cost())
                        command.allow_user(self.name)
                        command.increase_cost()
                        return f"@{self.name} bought !{effect}"
                    else:
                        return f"@{self.name} IS TOO BROKE TO AFFORD !{effect}"
        else:
            return f"@{self.name} - Out of Cool Points to Purchase with"

    def commands(self):
        return Command.for_user(self.name)

    def doc(self):
        return {
            "name": self.name,
            "street_cred": 0,
            "cool_points": 0,
            "health": 5,
        }

    def _find_or_create_user(self):
        user_result = self.db().search(Query().name == self.name)
        if user_result:
            print(f"WE GOT A USER: {user_result}")
            user_result = user_result[0]
            return user_result
        else:
            print(f"Creating New User: {self.doc()}")
            from tinyrecord import transaction

            with transaction(self.db()) as tr:
                tr.insert(self.doc())
            return self.doc()

    def street_cred(self):
        user = self._find_or_create_user()
        return user["street_cred"]

    def cool_points(self):
        user = self._find_or_create_user()
        return user["cool_points"]

    def remove_cool_points(self, amount=1):
        user = self._find_or_create_user()

        def decrease_cred():
            def transform(doc):
                doc["cool_points"] = doc["cool_points"] - amount

            return transform

        self.db().update(decrease_cred(), Query().name == self.name)

    def add_cool_points(self, amount=1):
        user = self._find_or_create_user()

        def increase_cred():
            def transform(doc):
                doc["cool_points"] = doc["cool_points"] + amount

            return transform

        self.db().update(increase_cred(), Query().name == self.name)

    def remove_street_cred(self, amount=1):
        user = self._find_or_create_user()

        def decrease_cred():
            def transform(doc):
                doc["street_cred"] = doc["street_cred"] - amount

            return transform

        self.db().update(decrease_cred(), Query().name == self.name)

    def add_street_cred(self, amount=1):
        user = self._find_or_create_user()

        def increase_cred():
            def transform(doc):
                doc["street_cred"] = doc["street_cred"] + amount

            return transform

        self.db().update(increase_cred(), Query().name == self.name)

    def remove_all_commands(self):
        user = self._find_or_create_user()
        for command in self.commands():
            Command(command).unallow_user(user)
