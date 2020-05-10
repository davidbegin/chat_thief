from tinydb import Query

from chat_thief.models.database import db_table
from chat_thief.prize_dropper import random_soundeffect
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.config.log import error, warning, success

from chat_thief.models.command import Command
from chat_thief.models.base_model import BaseModel


class User(BaseModel):
    table_name = "users"
    database_folder = ""
    database_path = "db/users.json"

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def count(cls):
        return len(cls.all())

    @classmethod
    def all(cls):
        return [user["name"] for user in cls.db().all()]

    @classmethod
    def richest(cls):
        users = [[user["name"], user["cool_points"]] for user in cls.db().all()]
        return sorted(users, key=lambda user: user[1])

    @classmethod
    def total_street_cred(cls):
        return sum([user["street_cred"] for user in cls.db().all()])

    @classmethod
    def total_cool_points(self):
        return sum([user["cool_points"] for user in self.db().all()])

    @classmethod
    def purge(cls):
        return cls.db().purge()

    # ====================================================================

    # We should set self.user here
    def __init__(self, name):
        self.name = name
        self._raw_user = self._find_or_create_user()

    # So this means, when we call, we find or init, thats fine!
    def user(self):
        return self._find_or_create_user()

    def stats(self):
        return f"@{self.name} - Mana: {self.mana()} | Street Cred: {self.street_cred()} | Cool Points: {self.cool_points()}"
        # return f"@{self.name} - Mana: {self.mana()} | Karma: {self.karma()} | Street Cred: {self.street_cred()} | Cool Points: {self.cool_points()}"

    def commands(self):
        return Command.for_user(self.name)

    # Seems like it should be factored away
    def street_cred(self):
        return self.user()["street_cred"]

    def cool_points(self):
        return self.user()["cool_points"]

    def mana(self):
        return self.user()["mana"]

    def update_mana(self, amount):
        return self._update_value("mana", amount)

    # The ride or dies you have
    def karma(self):
        user_result = self.db().search(Query().ride_or_die == self.name)
        return len(user_result)

    def kill(self):
        return self._update_value("mana", -self.mana())

    def revive(self):
        return self._set_value("mana", 5)

    def paperup(self, amount=100):
        self.update_street_cred(amount)
        self.update_cool_points(amount)
        return f"{self.name} has been Papered Up"

    def _find_affordable_random_command(self):
        looking_for_effect = True

        while looking_for_effect:
            # Should we update this query to take cost parameter?
            effect = random_soundeffect()
            # We need to check the cost
            command = Command(effect)
            if self.cool_points() >= command.cost() and not command.allowed_to_play(
                self.name
            ):
                looking_for_effect = False
        return command

    def buy(self, effect):
        if (
            effect != "random"
            and effect not in SoundeffectsLibrary.fetch_soundeffect_names()
        ):
            raise ValueError(f"Invalid Effect: {effect}")

        if self.cool_points() > 0:
            if effect == "random":
                command = self._find_affordable_random_command()
                self.update_cool_points(-command.cost())
                command.allow_user(self.name)
                command.increase_cost()
                return f"@{self.name} purchased: {command.name}"
            else:
                if Command(effect).allowed_to_play(self.name):
                    return f"@{self.name} already has access to !{effect}"
                else:
                    command = Command(effect)

                    if self.cool_points() >= command.cost():
                        self.update_cool_points(-command.cost())
                        command.allow_user(self.name)
                        command.increase_cost()
                        return f"@{self.name} bought !{effect}"
                    else:
                        return f"@{self.name} IS TOO BROKE TO AFFORD !{effect}"
        else:
            return f"@{self.name} - Out of Cool Points to Purchase with"

    # This is initial doc
    def doc(self):
        return {
            "name": self.name,
            "street_cred": 0,
            "cool_points": 0,
            "mana": 5,
        }

    def save(self):
        return self._find_or_create_user()

    def _find_or_create_user(self):
        user_result = self.db().search(Query().name == self.name)
        if user_result:
            user_result = user_result[0]
            return user_result
        else:
            success(f"Creating New User: {self.doc()}")
            from tinyrecord import transaction

            with transaction(self.db()) as tr:
                tr.insert(self.doc())
            return self.doc()

    def update_cool_points(self, amount=1):
        self._update_value("cool_points", amount)

    def update_street_cred(self, amount=1):
        self._update_value("street_cred", amount)

    def set_ride_or_die(self, ride_or_die):
        self._set_value("ride_or_die", ride_or_die)

    # ===========
    # Punishments
    # ===========

    def remove_all_commands(self):
        for command in self.commands():
            Command(command).unallow_user(self.name)

    def bankrupt(self):
        self.update_street_cred(-self.street_cred())
        self.update_cool_points(-self.cool_points())
        return f"{self.name} is now Bankrupt"
