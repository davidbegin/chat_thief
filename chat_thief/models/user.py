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

    # We should set self.user here
    def __init__(
        self,
        name,
        cool_points=0,
        notoriety=0,
        top_eight=[],
        custom_css=None,
        insured=False,
    ):
        self._top_eight = top_eight
        self.name = name
        self._cool_points = cool_points
        self._custom_css = custom_css
        self._notoriety = notoriety
        self._insured = insured
        self._raw_user = self._find_or_create_user()

    @classmethod
    def register_bot(cls, bot, creator):
        cls.db().upsert(
            {"is_bot": True, "creator": creator, "name": bot}, Query().name == bot
        )

    @classmethod
    def bots(cls):
        bots = cls.db().search(Query().is_bot)
        return [bot["name"] for bot in bots]

    @classmethod
    def all_data(cls):
        user_data = cls.db().all()
        cmd_data = Command.db().all()
        results = []

        all_sfxs = SoundeffectsLibrary.fetch_soundeffect_samples()

        for user_dict in user_data:
            matching_effects = [
                sfx
                for sfx in all_sfxs
                if user_dict["name"] == sfx.name[: -len(sfx.suffix)]
            ]
            if matching_effects:
                command_file = matching_effects[0]
                user_dict["command_file"] = command_file.name

            user_dict["commands"] = [
                cmd["name"]
                for cmd in cmd_data
                if user_dict["name"] in cmd["permitted_users"]
            ]
            results.append(user_dict)
        return results

    # We shouldn't use this all
    # @classmethod
    # def all(cls):
    #     return [user["name"] for user in cls.db().all()]

    @classmethod
    def total_street_cred(cls):
        return sum([user["street_cred"] for user in cls.db().all()])

    @classmethod
    def total_cool_points(self):
        return sum([user["cool_points"] for user in self.db().all()])

    @classmethod
    def richest(cls):
        users = [[user["name"], user["cool_points"]] for user in cls.db().all()]
        return sorted(users, key=lambda user: user[1])

    @classmethod
    def richest_street_cred(cls):
        users = [user for user in cls.db().all()]
        if users:
            return sorted(users, key=lambda user: user["street_cred"])[-1]

    @classmethod
    def richest_cool_points(cls):
        users = [user for user in cls.db().all()]
        if users:
            return sorted(users, key=lambda user: user["cool_points"])[-1]

    @classmethod
    def by_cool_points(cls):
        users = [user for user in cls.db().all()]
        if users:
            return reversed(sorted(users, key=lambda user: user["cool_points"]))

    # ====================================================================

    # So this means, when we call, we find or init, thats fine!
    def user(self):
        return self._find_or_create_user()

    def stats(self):
        return f"@{self.name} - Mana: {self.mana()} | Street Cred: {self.street_cred()} | Cool Points: {self.cool_points()} | Wealth: {self.wealth()} | Insured: {self.insured()}"

    def commands(self):
        return [
            permission["name"]
            for permission in Command.for_user(self.name)
            if permission["name"] != self.name
        ]

    # Seems like it should be factored away
    def street_cred(self):
        return self.user()["street_cred"]

    def cool_points(self):
        return self.user()["cool_points"]

    def custom_css(self):
        return self.user()["custom_css"]

    def mana(self):
        return self.user()["mana"]

    def is_bot(self):
        return self.user().get("is_bot", False)

    def creator(self):
        return self.user().get("creator", None)

    def notoriety(self):
        return self.user().get("notoriety", 0)

    def top_eight(self):
        return self.user().get("top_eight", [])

    def insured(self):
        return self.user().get("insured", False)

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
            # Should we update this query to take cost parameter?
            effect = random_soundeffect()
            # We need to check the cost
            command = Command(effect)
            if self.cool_points() >= command.cost() and not command.allowed_to_play(
                self.name
            ):
                looking_for_effect = False
        return command

    # Returning a string with the info
    # of what happened
    def buy(self, effect):
        if effect not in SoundeffectsLibrary.fetch_soundeffect_names():
            raise ValueError(f"Invalid Effect: {effect}")

        if Command(effect).allowed_to_play(self.name):
            return f"@{self.name} already has access to !{effect}"

        current_cool_points = self.cool_points()
        command = Command(effect)
        command_cost = command.cost()

        if current_cool_points >= command_cost:
            self.update_cool_points(-command_cost)
            command.allow_user(self.name)
            command.increase_cost()
            return f"@{self.name} bought !{effect} for {command_cost} Cool Points"
        else:
            return f"@{self.name} not enough Cool Points to buy !{effect} - {current_cool_points}/{command_cost}"

    # This is initial doc
    def doc(self):
        return {
            "name": self.name,
            "custom_css": self._custom_css,
            "notoriety": self._notoriety,
            "street_cred": 0,
            "cool_points": self._cool_points,
            "mana": 3,
            "top_eight": self._top_eight,
            "insured": self._insured,
        }

    def _find_or_create_user(self):
        # We should be using get
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

    def clear_top_eight(self):
        self.set_value("top_eight", [])

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
