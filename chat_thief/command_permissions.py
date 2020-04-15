from pathlib import Path
import traceback

from tinydb import TinyDB, Query

from chat_thief.models import User, SoundEffect, CommandPermission
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.irc import send_twitch_msg
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee

db_location = "db/soundeffects.json"
soundeffects_db_path = Path(__file__).parent.parent.joinpath(db_location)
DB = TinyDB(soundeffects_db_path)
COMMAND_PERMISSIONS_TABLE = DB.table("command_permissions")


class CommandPermissionCenter:
    def __init__(self, user, command, args, db_location="db/soundeffects.json"):
        self.user = user
        self.command = command
        self.args = args

    @staticmethod
    def fetch_whitelisted_users():
        return (
            Path(__file__)
            .parent.parent.joinpath(".whitelisted_users")
            .read_text()
            .split()
        )

    # You could pass nothing, then I look the permissions for the user
    # if you pass in someone whose in the chat (according to welcome), then
    # their permissions
    # If you pass in a command, what users have permission for that command command permissions
    def fetch_permissions(self):
        # Return the users permissions
        if not self.args:
            send_twitch_msg(
                f"@{self.user}'s Permissions: {self.fetch_user_permissions()}"
            )
        elif self.command in WelcomeCommittee.fetch_present_users():
            send_twitch_msg(
                f"!{self.args[0]}'s Permissions: {self.fetch_user_permissions(self.args[0])}"
            )
        else:
            permissions = CommandPermissionCenter.permissions_for_command(self.args[0])
            send_twitch_msg(f"!{self.args[0]}'s Permissions: {permissions}")
            # We need to check if it is user

    def _is_theme_song(self):
        return self.command in SoundeffectsLibrary.fetch_theme_songs()

    def _is_personal_theme_song(self):
        return self._is_theme_song() and self.user == self.command

    @staticmethod
    def permissions_for_command(command):
        if command in SoundeffectsLibrary.fetch_theme_songs():
            return [command]

        if command == "snorlax":
            return ["snorlax"]

        if result := COMMAND_PERMISSIONS_TABLE.search(Query().command == command):
            return result[-1]["permitted_users"]
        else:
            return ["Stream Lords"]
            # print("Defaulting to STREAM_LORDS")

    def fetch_command_permissions(self):
        print(f"Looking for command: {self.command}")

        if self._is_personal_theme_song() and self._is_theme_song():
            return [self.user]

        if not self._is_personal_theme_song() and self._is_theme_song():
            return []

        if self.command == "snorlax" and self.user == "artmattdank":
            return ["snorlax"]

        if result := COMMAND_PERMISSIONS_TABLE.search(Query().command == self.command):
            return result[-1]["permitted_users"]
        else:
            return ["Stream Lords"]

    def fetch_user_permissions(self, user=None):
        if user is None:
            user = self.user

        def test_func(permitted_users, current_user):
            return current_user in permitted_users

        if user in STREAM_LORDS:
            return ["All Commands!"]
        else:
            return [
                permission["command"]
                for permission in COMMAND_PERMISSIONS_TABLE.search(
                    Query().permitted_users.test(test_func, user)
                )
            ]

    def add_perm(self):
        try:
            if self.user in STREAM_LORDS:
                return self.add_permission()
            else:
                allowed_commands = self.fetch_user_permissions()
                if self.command in allowed_commands:
                    print(f"{self.user} CAN ADD")
                else:
                    print(f"{self.user} cannot add permissions")
        except Exception as e:
            trace = traceback.format_exc()
            print(f"Error adding permission: {e} {trace}")

    # This self.args thing might be wrong
    # or I think it is wrong
    # Its implying we only want to add permissions
    # from chat
    def add_permission(self):
        # WE need to check if these are valid users
        # Maybe by the welcome list
        for user in self.args:
            self.add_permission_for_user(user)

    def add_permission_for_user(self, user):
        print(f"\nAttempting To Add Permission: {self.args[0]} for {user}")

        # Find the previous permission configuration
        command_config = COMMAND_PERMISSIONS_TABLE.search(
            Query().command == self.args[0]
        )

        if command_config:
            command_config = command_config[-1]
            command_config["permitted_users"].append(user)
            print(f"Updating Previous Command Permissions {command_config.__dict__}")
            COMMAND_PERMISSIONS_TABLE.update(command_config)
        else:
            command_permission = CommandPermission(
                user=user, command=self.args[0], permitted_users=[user],
            )
            print(f"Adding Initial Command Permissions {command_permission.__dict__}")
            COMMAND_PERMISSIONS_TABLE.insert(command_permission.__dict__)
