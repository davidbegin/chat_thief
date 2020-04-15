from pathlib import Path
import traceback

from tinydb import TinyDB, Query

from chat_thief.models import User, SoundEffect, CommandPermission
from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.irc import send_twitch_msg
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee

TABLE_NAME = "command_permissions"


# This handles wayyyy too much
# We need to separate out the logic and clean up abstractions


def _command_permissions_table(db_location):
    soundeffects_db_path = Path(__file__).parent.parent.joinpath(db_location)
    return TinyDB(soundeffects_db_path).table(TABLE_NAME)


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
        self.table = _command_permissions_table(db_location)
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

        user_permissions = list(set(user_permissions))
        if user_permissions:
            send_twitch_msg(f"{title} Permissions: {user_permissions}")
        else:
            pass

    # There are 2 concepts
    # Fetch command permission
    # fetch command permissions for a user
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
        def in_permitted_users(permitted_users, current_user):
            return current_user in permitted_users

        command_permissions = [
            permission["command"]
            for permission in self.table.search(
                Query().permitted_users.test(in_permitted_users, self.user)
            )
        ]
        if self._has_theme_song():
            return command_permissions + [self.user]
        return command_permissions

    def add_perm(self):
        try:
            if self.user in STREAM_GODS:
                return self._add_permission()
            else:
                allowed_commands = self.fetch_user_permissions()
                if (
                    self.args[0] in allowed_commands
                    and self.args[0] is not SoundeffectsLibrary.fetch_theme_songs()
                ):
                    return self._add_permission()
                else:
                    print(f"{self.user} cannot add permissions")
        except Exception as e:
            trace = traceback.format_exc()
            print(f"Error adding permission: {e} {trace}")

    def _add_permission(self):
        if len(self.args) < 2:
            print("you need more args!")
            return

        print(f"\nAttempting To Add Permission: {self.args[0]}")
        if command_config := self.table.search(Query().command == self.args[0]):
            print("Updating Permission")
            self._update_permissions(command_config[-1])
        else:
            print("New Permission")
            self._new_permissions()

    def _new_permissions(self):
        if self._validate_user(self.args[1]):
            command_permission = CommandPermission(
                user=self.user, command=self.args[0], permitted_users=[self.args[1]],
            )
            print(f"Adding Initial Command Permissions {command_permission.__dict__}")
            self.table.insert(command_permission.__dict__)

    def _update_permissions(self, command_config):
        if self._validate_user(self.args[1]):

            if self.args[1] not in command_config["permitted_users"]:
                command_config["permitted_users"].append(self.args[1])
                print(
                    f"Updating Previous Command Permissions {command_config.__dict__}"
                )
                self.table.update(command_config)
            else:
                print(f"{self.args[1]} already has that command: {self.args[0]}!")

    def _validate_user(self, user):
        if self.skip_validation:
            print("Skipping Validation for adding user permissions")
            return True

        user_eligible_for_permissions = (
            # user not in STREAM_LORDS
            user in WelcomeCommittee.fetch_present_users()
            and self.command not in SoundeffectsLibrary.fetch_theme_songs()
        )
        if not user_eligible_for_permissions:
            print("This user is not eligible for permissions")
        return user_eligible_for_permissions

    def _has_theme_song(self):
        return self.user in SoundeffectsLibrary.fetch_theme_songs()

    def _is_theme_song(self):
        return self.command in SoundeffectsLibrary.fetch_theme_songs()

    def _is_personal_theme_song(self):
        return self._is_theme_song() and self.user == self.command
