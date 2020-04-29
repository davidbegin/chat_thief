from tinydb import Query

from chat_thief.models.database import db_table
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.config.stream_lords import STREAM_GODS


class Command:
    table_name = "commands"
    database_folder = ""
    database_path = "db/commands.json"

    def __init__(self, name):
        self.name = name
        self.permitted_users = []
        self.health = 5
        self.is_theme_song = self.name in SoundeffectsLibrary.fetch_theme_songs()

    def _new_command(self, permitted_users=[]):
        return {
            "command": self.name,
            "user": "beginbot",
            "permitted_users": permitted_users,
            "health": self.health,
        }

    @classmethod
    def db(cls):
        return db_table(cls.database_folder + cls.database_path, cls.table_name)

    @classmethod
    def count(cls):
        return len(cls.db().all())

    def allowed_to_play(self, user):
        if self.is_theme_song:
            return user == self.name

        if user in STREAM_GODS:
            return True

        if command := self.db().get(Query().command == self.name):
            return user in command["permitted_users"]

        return False

    def unallow_user(self, target_user):
        command = self.db().get(Query().command == self.name)

        if command:
            self._remove_user(target_user)
            return f"@{target_user} lost access to !{self.name}"
        else:
            return f"No One has accesss to !{self.name}"

    def allow_user(self, target_user):
        command = self.db().get(Query().command == self.name)

        if command:
            if target_user not in command["permitted_users"]:
                self._add_user(target_user)
                return f"@{target_user} now has access to !{self.name}"
            else:
                return f"@{target_user} already allowed !{self.name}"
        else:
            self._create_new_command(target_user)
            return f"@{target_user} is the 1st person with access to: !{self.name}"

    def users(self):
        if command := self.db().get(Query().command == self.name):
            return command["permitted_users"]
        else:
            return None

    def _create_new_command(self, target_user):
        from tinyrecord import transaction

        with transaction(self.db()) as tr:
            tr.insert(self._new_command(permitted_users=[target_user]))

    def _add_user(self, target_user):
        def add_permitted_users():
            def transform(doc):
                doc["permitted_users"].append(target_user)

            return transform

        self.db().update(add_permitted_users(), Query().command == self.name)

    def _remove_user(self, target_user):
        def remove_permitted_users():
            def transform(doc):
                doc["permitted_users"].remove(target_user)

            return transform

        self.db().update(remove_permitted_users(), Query().command == self.name)

    def _user_has_chatted(self):
        # if not self.skip_validation:
        #     if target_user not in WelcomeCommittee().present_users():
        #         raise ValueError(f"Not a valid user: {target_user}")
        pass
