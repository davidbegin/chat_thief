from chat_thief.stream_lords import STREAM_LORDS

from tinydb import TinyDB, Query
from pathlib import Path

from chat_thief.models import User, SoundEffect, CommandPermission


def fetch_whitelisted_users():
    return (
        Path(__file__).parent.parent.joinpath(".whitelisted_users").read_text().split()
    )


class CommandPermissionCenter:
    def __init__(self, db_location="db/soundeffects.json"):
        soundeffects_db_path = Path(__file__).parent.parent.joinpath(db_location)
        DB = TinyDB(soundeffects_db_path)
        self.command_permissions_table = DB.table("command_permissions")

    def fetch_command_permissions(self, command):
        print(f"Looking for command: {command}")
        if result := self.command_permissions_table.search(Query().command == command):
            return result[-1]["permitted_users"]
        else:
            print("Defaulting to STREAM_LORDS")
            return STREAM_LORDS

    def fetch_user_permissions(self, user):
        def test_func(permitted_users, user):
            return user in permitted_users

        return [
            permission["command"]
            for permission in self.command_permissions_table.search(
                Query().permitted_users.test(test_func, user)
            )
        ]

    def add_perm(self, command):
        try:
            if self.user in STREAM_LORDS:
                return self.command_permission_center.add_permission(self.msg)
            else:
                allowed_commands = CommandPermissionCenter().fetch_user_permissions(
                    self.user
                )
                if command in allowed_commands:
                    print(f"{self.user} CAN ADD")
                else:
                    print(f"{self.user} cannot add permissions")
        except Exception as e:
            trace = traceback.format_exc()
            print(f"Error adding permission: {e} {trace}")

    def add_permission(self, raw_msg):
        _, command, *users = raw_msg.strip().split(" ")

        # TODO: fix this
        for user in users:
            self.add_permission_for_user(user, command)

    def add_permission_for_user(self, user, command):
        print(f"\nAttempting To Add Permission: {command} for {user}")

        # Find the previous permission configuration
        command_config = self.command_permissions_table.search(
            Query().command == command
        )

        if command_config:
            command_config = command_config[-1]
            command_config["permitted_users"].append(user)
            print(f"Updating Previous Command Permissions {command_config.__dict__}")
            self.command_permissions_table.update(command_config)
        else:
            command_permission = CommandPermission(
                user=user, command=command, permitted_users=STREAM_LORDS + [user]
            )
            print(f"Adding Initial Command Permissions {command_permission.__dict__}")
            self.command_permissions_table.insert(command_permission.__dict__)
