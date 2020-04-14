from pathlib import Path
import traceback

from tinydb import TinyDB, Query

from chat_thief.models import User, SoundEffect, CommandPermission
from chat_thief.stream_lords import STREAM_LORDS


class CommandPermissionCenter:
    def __init__(self, user, command, args, db_location="db/soundeffects.json"):
        self.user = user
        self.command = command
        self.args = args
        soundeffects_db_path = Path(__file__).parent.parent.joinpath(db_location)
        DB = TinyDB(soundeffects_db_path)
        self.command_permissions_table = DB.table("command_permissions")

    @staticmethod
    def fetch_whitelisted_users():
        return (
            Path(__file__)
            .parent.parent.joinpath(".whitelisted_users")
            .read_text()
            .split()
        )

    def fetch_command_permissions(self):
        print(f"Looking for command: {self.command}")
        if result := self.command_permissions_table.search(
            Query().command == self.command
        ):
            return result[-1]["permitted_users"]
        else:
            print("Defaulting to STREAM_LORDS")
            return STREAM_LORDS

    def fetch_user_permissions(self):
        def test_func(permitted_users, current_user):
            return current_user in permitted_users

        return [
            permission["command"]
            for permission in self.command_permissions_table.search(
                Query().permitted_users.test(test_func, self.user)
            )
        ]

    def add_perm(self):
        try:
            if self.user in STREAM_LORDS:
                return self.command_permission_center.add_permission()
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
        print(f"\nAttempting To Add Permission: {self.command} for {self.user}")

        # Find the previous permission configuration
        command_config = self.command_permissions_table.search(
            Query().command == self.command
        )

        if command_config:
            command_config = command_config[-1]
            command_config["permitted_users"].append(self.user)
            print(f"Updating Previous Command Permissions {command_config.__dict__}")
            self.command_permissions_table.update(command_config)
        else:
            command_permission = CommandPermission(
                user=self.user,
                command=self.command,
                permitted_users=STREAM_LORDS + [self.user],
            )
            print(f"Adding Initial Command Permissions {command_permission.__dict__}")
            self.command_permissions_table.insert(command_permission.__dict__)
