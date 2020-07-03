from tinydb import Query

from chat_thief.models.database import db_table
from chat_thief.prize_dropper import random_soundeffect
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary
from chat_thief.config.log import error, warning, success
from chat_thief.models.command import Command
from chat_thief.models.base_db_model import BaseDbModel


class User(BaseDbModel):
    table_name = "users"
    database_path = "db/users.json"

    def __init__(
        self, name, cool_points=0, top_eight=[], custom_css=None, insured=False,
    ):
        self._top_eight = top_eight
        self.name = name
        self._cool_points = cool_points
        self._custom_css = custom_css
        self._insured = insured
        self._raw_user = self._find_or_create_user()

    @classmethod
    def register_bot(cls, bot, creator):
        cls.db().upsert(
            {"is_bot": True, "creator": creator, "name": bot}, Query().name == bot
        )

    @classmethod
    def bots(cls):
        return [
            # bot["name"] for bot in cls.db().search(Query().is_bot)
            bot["name"]
            for bot in cls.db().search(Query().is_bot == True)
        ]

    @classmethod
    def total_street_cred(cls):
        return cls._total_of_field("street_cred")

    @classmethod
    def total_cool_points(cls):
        return cls._total_of_field("cool_points")

    @classmethod
    def _total_of_field(cls, field):
        return sum([user[field] for user in cls.db().all()])

    @classmethod
    def richest_street_cred(cls):
        return cls.max_of_field("street_cred")

    @classmethod
    def richest_cool_points(cls):
        return cls.max_of_field("cool_points")

    @classmethod
    def max_of_field(cls, field):
        users = [user for user in cls.db().all()]
        if users:
            return sorted(users, key=lambda user: user[field])[-1]

    @classmethod
    def by_cool_points(cls):
        users = [user for user in cls.db().all()]
        if users:
            return reversed(sorted(users, key=lambda user: user["cool_points"]))

    @classmethod
    def richest(cls):
        users = [[user["name"], user["cool_points"]] for user in cls.db().all()]
        return sorted(users, key=lambda user: user[1])

    # ====================================================================

    # So this means, when we call, we find or init, thats fine!
    def user(self):
        return self._find_or_create_user()

    def stats(self):
        return (
            f"@{self.name} - Mana: {self.mana()} | "
            f"Street Cred: {self.street_cred()} | "
            f"Cool Points: {self.cool_points()} | "
            f"Wealth: {self.wealth()} | "
            f"Insured: {self.insured()}"
        )

    def commands(self):
        return [
            permission["name"]
            for permission in Command.for_user(self.name)
            if permission["name"] != self.name
        ]

    # =====================================

    # Seems like it should be factored away
    def street_cred(self):
        return self._fetch_field("street_cred", 0)

    def cool_points(self):
        return self._fetch_field("cool_points", 0)

    def custom_css(self):
        return self._fetch_field("custom_css", None)

    def mana(self):
        return self._fetch_field("mana", 0)

    def is_bot(self):
        return self._fetch_field("is_bot", False)

    def creator(self):
        return self._fetch_field("creator", None)

    def top_eight(self):
        return self._fetch_field("top_eight", [])

    def insured(self):
        return self._fetch_field("insured", False)

    def _fetch_field(self, field, default):
        return self.user().get(field, default)

    # =============================================

    def update_mana(self, amount):
        return self._update_value("mana", amount)

    # The ride or dies you have
    def karma(self):
        user_result = self.db().search(Query().ride_or_die == self.name)
        return len(user_result)

    def kill(self):
        return self._update_value("mana", -self.mana())

    def revive(self, mana=3):
        return self.set_value("mana", mana)

    def paperup(self, amount=100):
        self.update_street_cred(amount)
        self.update_cool_points(amount)
        return f"@{self.name} has been Papered Up"

    # This also might need a quick exit
    def _find_affordable_random_command(self):
        if self.cool_points() < 1:
            raise ValueError("You can't afford anything!")

        looking_for_effect = True

        while looking_for_effect:
            effect = random_soundeffect()
            command = Command(effect)
            if self.cool_points() >= command.cost() and not command.allowed_to_play(
                self.name
            ):
                looking_for_effect = False
        return command

    # This is initial doc
    def doc(self):
        return {
            "name": self.name,
            "custom_css": self._custom_css,
            "street_cred": 0,
            "cool_points": self._cool_points,
            "mana": 3,
            "top_eight": self._top_eight,
            "insured": self._insured,
        }

    def _find_or_create_user(self):
        user_result = self.db().get(Query().name == self.name)
        if user_result:
            return user_result
        else:
            success(f"Creating New User: {self.doc()}")
            from tinyrecord import transaction

            with transaction(self.db()) as tr:
                tr.insert(self.doc())
            return self.doc()

    def update_cool_points(self, amount=1):
        return self._update_value("cool_points", amount)

    def update_street_cred(self, amount=1):
        return self._update_value("street_cred", amount)

    def clear_top_eight(self):
        self.set_value("top_eight", [])

    def set_ride_or_die(self, ride_or_die):
        if ride_or_die != self.name:
            return self.set_value("ride_or_die", ride_or_die)

    def add_to_top_eight(self, friend):
        current_eight = self.top_eight()

        if len(current_eight) == 8:
            raise ValueError("You can only have 8 in your Top 8!")

        if friend not in current_eight and len(current_eight) < 8:
            current_eight.append(friend)
            self.set_value("top_eight", current_eight)

    def remove_from_top_eight(self, enemy):
        current_eight = self.top_eight()
        if enemy in current_eight:
            current_eight.remove(enemy)
            self.set_value("top_eight", current_eight)

    def top_wealth(self):
        user_data = self.user()
        user_commands = Command.for_user(self.name)
        total_command_wealth = sum([command["cost"] for command in user_commands])
        return user_data["cool_points"] + total_command_wealth

    @classmethod
    def wealthiest(cls):
        richest = [
            (user["name"], User(user["name"]).top_wealth()) for user in cls.db().all()
        ]

        return sorted(richest, key=lambda user: user[1])[-1][0]

    def remove_all_commands(self):
        for command in self.commands():
            Command(command).unallow_user(self.name)

    def bankrupt(self):
        self.update_street_cred(-self.street_cred())
        self.update_cool_points(-self.cool_points())
        return f"@{self.name} is now Bankrupt"

    def wealth(self):
        return (
            sum([Command(command).cost() for command in self.commands()])
            + self.cool_points()
        )

    def buy_insurance(self):
        current_cool_points = self.cool_points()
        if current_cool_points > 0:
            cool_points = current_cool_points - 1
            self.db().upsert(
                {"cool_points": cool_points, "insured": True}, Query().name == self.name
            )
            return f"@{self.name} thank you for purchasing insurance"
        else:
            return f"YA Broke @{self.name} - it costs 1 Cool Point to buy insurance"
