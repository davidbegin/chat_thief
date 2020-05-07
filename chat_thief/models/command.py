import traceback
import os
from collections import Counter
from itertools import chain

from tinydb import Query

from chat_thief.models.database import db_table
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.models.sfx_vote import SFXVote


class Command:
    table_name = "commands"
    database_folder = ""
    database_path = "db/commands.json"

    def __init__(self, name):
        self.name = name
        self.permitted_users = []
        self.health = 5
        self.inital_cost = 1
        self.is_theme_song = self.name in SoundeffectsLibrary.fetch_theme_songs()

    @classmethod
    def find_or_create(cls, name):
        found_command = cls.db().get(Query().command == name)

        if found_command:
            return found_command
        else:
            return cls(name)._create_new_command()

    @classmethod
    def for_user(cls, user):
        def in_permitted_users(permitted_users, current_user):
            return current_user in permitted_users

        return [
            permission["command"]
            for permission in cls.db().search(
                Query().permitted_users.test(in_permitted_users, user)
            )
        ]

    @classmethod
    def most_popular(cls):
        result = cls.db().all()
        sorted_commands = sorted(result, key=lambda command: command["cost"])
        return [
            f"{command['command']}: {command['cost']}"
            for command in sorted_commands[-5:]
        ]

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def count(cls):
        return len(cls.db().all())

    def exists(self):
        return cls.db().get(Query().command == name) is not None

    def allowed_to_play(self, user):
        if not SFXVote(self.name).is_enabled():
            print(f"{self.name} is not currently enabled")
            return False

        if self.is_theme_song:
            return user == self.name

        if user in STREAM_GODS:
            return True

        if command := self.db().get(Query().command == self.name):
            return user in command["permitted_users"]

        return False

    def cost(self):
        if command := self.db().get(Query().command == self.name):
            return command["cost"]
        else:
            return 1

    def silence(self):
        def _db_remove_health():
            def transform(doc):
                doc["health"] = 0

        return self.db().update(_db_remove_health(), Query().command == self.name)

    def increase_cost(self, amount=1):
        if command := self.db().get(Query().command == self.name):
            self._increase_cost(amount)

    def _increase_cost(self, amount):
        def _db_increase_cost():
            def transform(doc):
                doc["cost"] = int(doc["cost"]) + int(amount)

            return transform

        self.db().update(_db_increase_cost(), Query().command == self.name)

    def unallow_user(self, target_user):
        try:
            command = self.db().get(Query().command == self.name)

            if command:
                self._remove_user(target_user)
                return f"@{target_user} lost access to !{self.name}"
            else:
                return f"No One has accesss to !{self.name}"
        except ValueError:
            if "TEST_MODE" in os.environ:
                traceback.print_exc()

    def allow_user(self, target_user):
        command = self.db().get(Query().command == self.name)

        if command:
            # What if we are none
            if target_user not in command["permitted_users"]:
                self._add_user(target_user)
                return f"@{target_user} now has access to !{self.name}"
            else:
                return f"@{target_user} already allowed !{self.name}"
        else:
            self._create_new_command([target_user])
            return f"@{target_user} is the 1st person with access to: !{self.name}"

    def users(self):
        if command := self.db().get(Query().command == self.name):
            return command["permitted_users"]
        else:
            return []

    def _create_new_command(self, target_users=[]):
        from tinyrecord import transaction

        new_command = self._new_command(permitted_users=target_users)
        with transaction(self.db()) as tr:
            tr.insert(new_command)
        return new_command

    def save(self):
        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.insert(
                {
                    "command": self.name,
                    "user": "beginbot",
                    "permitted_users": self.permitted_users,
                    "health": self.health,
                    "cost": self.inital_cost,
                }
            )

    def _add_user(self, target_user):
        def add_permitted_users():
            def transform(doc):
                doc["permitted_users"].append(target_user)

            return transform

        self.db().update(add_permitted_users(), Query().command == self.name)

    def _remove_user(self, target_user):
        def remove_permitted_users():
            def transform(doc):
                if target_user in doc["permitted_users"]:
                    doc["permitted_users"].remove(target_user)

            return transform

        self.db().update(remove_permitted_users(), Query().command == self.name)

    def _new_command(self, permitted_users=[]):
        return {
            "command": self.name,
            "user": "beginbot",
            "permitted_users": permitted_users,
            "health": self.health,
            "cost": self.inital_cost,
        }

    # def _user_has_chatted(self):
    #     if not self.skip_validation:
    #         if target_user not in WelcomeCommittee().present_users():
    #             raise ValueError(f"Not a valid user: {target_user}")
