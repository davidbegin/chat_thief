from pathlib import Path

from tinydb import TinyDB, Query

from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.audio_player import AudioPlayer
from chat_thief.models.command_permission import CommandPermission
from chat_thief.irc import send_twitch_msg
from chat_thief.welcome_file import WelcomeFile
from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.database import db_table, USERS_DB_PATH, COMMANDS_DB_PATH

BEGINBOTS = ["beginbot", "beginbotbot"]


class AudioCommand:
    def __init__(
        self,
        name,
        skip_validation=False,
        users_db_path=USERS_DB_PATH,
        commands_db_path=COMMANDS_DB_PATH,
    ):
        self.name = name
        self.skip_validation = skip_validation
        self.soundfile = SoundeffectsLibrary.find_sample(name)
        self.is_theme_song = self.name in SoundeffectsLibrary.fetch_theme_songs()

        self.users_db = db_table(users_db_path, "users")
        self.commands_db = db_table(commands_db_path, "commands")

    def play_sample(self, remove_health=False):
        AudioPlayer.play_sample(self.soundfile.resolve())

        # At this point, we think we have checked the permissions properly
        # So we need to check and remove Health
        if remove_health:
            print(f"\n\tSearching for {self.name}")
            command = self.commands_db.search(Query().command == self.name)
            print(f"\n\tCommand {command}")
            if command:
                health = command[0].get("health", 5)
                print(f"Health for {self.name} {health}")
            else:
                return "NO Command found"

            if health > 0:
                # AudioPlayer.play_sample(self.soundfile.resolve())
                print("I would have made a sound")
            else:
                print(f"{self.name} is out of health")
        else:
            print("I would have made a sound")
            # AudioPlayer.play_sample(self.soundfile.resolve())

    def allowed_to_play(self, user):
        if self.is_theme_song:
            return user == self.name

        if user in STREAM_GODS:
            return True

        # Sorry STREAM_LORDS
        # if user in STREAM_LORDS:
        #     return True

        if command_permission := self.commands_db.search(Query().command == self.name):
            return user in command_permission[-1]["permitted_users"]

        return False

    def permitted_users(self):
        if command_permission := self.commands_db.search(Query().command == self.name):
            return command_permission[-1]["permitted_users"]
        else:
            return []

    def unallow_user(self, target_user):
        command_permission = self.commands_db.search(Query().command == self.name)
        if command_permission:
            command_permission = command_permission[-1]

            def remove_users():
                def transform(doc):
                    doc["permitted_users"].remove(target_user)

                return transform

            self.commands_db.update(remove_users(), Query().command == self.name)

            return f"@{target_user} no longer allowed {self.name}"

        else:
            return f"No one had permission to {self.name}"

    def allow_user(self, target_user):
        if not self.skip_validation:
            if target_user not in WelcomeFile.present_users():
                raise ValueError(f"Not a valid user: {target_user}")

        command_permission = self.commands_db.search(Query().command == self.name)
        if command_permission:
            command_permission = command_permission[-1]

            if target_user not in command_permission["permitted_users"]:
                print(
                    f"Updating Previous Command Permissions {command_permission.__dict__}"
                )

                def add_permitted_users():
                    def transform(doc):
                        doc["permitted_users"].append(target_user)

                    return transform

                self.commands_db.update(
                    add_permitted_users(), Query().command == self.name
                )

                message = (
                    f"User @{target_user} updated permissions for command: {self.name}"
                )
            else:
                message = f"User @{target_user} is already in permitted_users for {self.name}!"
        else:
            command_permission = CommandPermission(
                user="beginbot", command=self.name, permitted_users=[target_user],
            )
            print(f"Creating New Command Permissions: {command_permission.__dict__}")
            from tinyrecord import transaction

            with transaction(self.commands_db) as tr:
                tr.insert(command_permission.__dict__)
            message = f"User @{target_user} is the first person wh access to the command: !{self.name}"

        return message
