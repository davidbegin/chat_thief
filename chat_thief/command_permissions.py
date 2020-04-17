from pathlib import Path
import traceback

from tinydb import TinyDB, Query

from chat_thief.models import SoundEffect, CommandPermission
from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.irc import send_twitch_msg
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models import _command_permissions_table, DEFAULT_DB_LOCATION
from chat_thief.user import User


def fetch_whitelisted_users():
    return (
        Path(__file__)
        .parent.parent.joinpath("db/.whitelisted_users")
        .read_text()
        .split()
    )


class CommandPermissionCenter:
    def __init__(
        self,
        user,
        command=None,
        args=[],
        db_location="db/soundeffects.json",
        skip_validation=False,
    ):
        self.user = user
        self.command = command
        self.args = args
        self.commands_db_path = db_location
        self.table = _command_permissions_table(DEFAULT_DB_LOCATION)
        self.skip_validation = skip_validation

    @classmethod
    def fetch_permissions(cls, user, args=[]):
        user_permissions = []

        if not args:
            title = f"@{user}'s"
            user_permissions = cls(user=user).fetch_user_permissions()
        elif args[0] in WelcomeCommittee.fetch_present_users():
            title = f"@{args[0]}'s"
            user_permissions = cls(user=args[0]).fetch_user_permissions()
        elif args[0] in SoundeffectsLibrary.fetch_soundeffect_names():
            if len(args) > 1:
                for arg in args[1:]:
                    if arg in WelcomeCommittee.fetch_present_users():
                        title = f"@{arg}'s"
                        user_permissions = cls(
                            user=arg, command=args[0]
                        ).fetch_user_permissions()
            else:
                title = f"!{args[0]}'s"
                user_permissions = cls(
                    user=None, command=args[0]
                ).fetch_command_permissions()
        else:
            print("Not sure what to do!!!")
            return

        if user in STREAM_LORDS:
            title = f"Stream Lord: {title}"

        # This is a hack
        # user_permissions = list(set(user_permissions))
        if user_permissions:
            send_twitch_msg(f"{title} Permissions: {user_permissions}")
        else:
            pass

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

        if result := self.table.search(Query().command == self.command):
            return result[-1]["permitted_users"]
        else:
            return []

    def fetch_user_permissions(self):
        command_permissions = User(
            self.user, commands_db_path=self.commands_db_path
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
