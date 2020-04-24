from pathlib import Path

from tinydb import Query

from chat_thief.models.database import db_table, USERS_DB_PATH, COMMANDS_DB_PATH
from chat_thief.irc import send_twitch_msg
from chat_thief.models.soundeffect import SoundEffect
from chat_thief.models.command_permission import CommandPermission
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.models.user import User
from chat_thief.welcome_file import WelcomeFile


def fetch_whitelisted_users():
    return (
        Path(__file__)
        .parent.parent.joinpath("db/.whitelisted_users")
        .read_text()
        .split()
    )


class PermissionsFetcher:
    def __init__(
        self,
        user,
        command=None,
        commands_db_path=COMMANDS_DB_PATH,
        users_db_path=USERS_DB_PATH,
        skip_validation=False,
    ):
        self.user = user
        self.command = command
        self.skip_validation = skip_validation
        self.commands_db_path = commands_db_path
        self.users_db_path = users_db_path
        self.users_db = db_table(users_db_path, "users")
        self.commands_db = db_table(commands_db_path, "commands")

    @classmethod
    def fetch_permissions(cls, user, target_command, target_user):
        user_permissions = []

        if not target_command and not target_user:
            title = f"@{user}'s"
            user_permissions = cls(user=user).fetch_user_permissions()
            user_permissions = " ".join([f"!{perm}" for perm in user_permissions])
        elif target_user and not target_command:
            title = f"@{target_user}'s"
            user_permissions = cls(user=target_user).fetch_user_permissions()
            user_permissions = " ".join([f"!{perm}" for perm in user_permissions])
        elif target_command and not target_user:
            title = f"!{target_command}'s"
            user_permissions = cls(
                user=None, command=target_command
            ).fetch_command_permissions()

            if not user_permissions:
                title = f"No One can use !{target_command}"
            user_permissions = " ".join([f"@{perm}" for perm in user_permissions])
        elif target_command and target_user:
            title = f"@{target_user} !{target_command}"
            user_permissions = cls(
                user=target_user, command=target_command
            ).fetch_user_permissions()

        if target_user in STREAM_LORDS or user in STREAM_LORDS:
            title = f"👑 Stream Lord 👑: {title}"

        return f"{title} Permissions: {user_permissions}"

    def purge(self):
        self.commands_db.purge()

    def fetch_command_permissions(self):
        print(f"Looking for command: {self.command}")

        if self._is_personal_theme_song() and self._is_theme_song():
            return [self.user]

        if not self._is_personal_theme_song() and self._is_theme_song():
            return []

        if self.command == "snorlax" and self.user == "artmattdank":
            return ["snorlax"]

        if self.user in STREAM_LORDS:
            return [self.user]

        if result := self.commands_db.search(Query().command == self.command):
            return result[-1]["permitted_users"]
        else:
            return []

    def fetch_user_permissions(self):
        command_permissions = User(
            self.user,
            commands_db_path=self.commands_db_path,
            users_db_path=self.users_db_path,
        ).commands()

        if self._has_theme_song():
            return command_permissions + [self.user]
        return command_permissions

    def _has_theme_song(self):
        return self.user in SoundeffectsLibrary.fetch_theme_songs()

    def _is_theme_song(self):
        return self.command in SoundeffectsLibrary.fetch_theme_songs()

    def _is_personal_theme_song(self):
        return self._is_theme_song() and self.user == self.command
