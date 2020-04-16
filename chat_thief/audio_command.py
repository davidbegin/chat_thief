from pathlib import Path

from tinydb import TinyDB, Query

from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.audio_player import AudioPlayer
from chat_thief.models import CommandPermission
from chat_thief.irc import send_twitch_msg
from chat_thief.welcome_committee import WelcomeCommittee

from chat_thief.stream_lords import STREAM_LORDS

from chat_thief.models import _command_permissions_table, DEFAULT_DB_LOCATION


class AudioCommand:
    def __init__(self, name, skip_validation=False, db_location=DEFAULT_DB_LOCATION):
        self.name = name
        self.skip_validation = skip_validation
        self.db_location = db_location
        self.soundfile = SoundeffectsLibrary.find_sample(name)
        self.is_theme_song = self.name in SoundeffectsLibrary.fetch_theme_songs()
        self.table = _command_permissions_table(db_location)

    def play_sample(self):
        AudioPlayer.play_sample(self.soundfile.resolve())

    def allowed_to_play(self, user):
        if self.is_theme_song:
            return user == self.name

        if user in STREAM_LORDS:
            return True

        command_permission = self.table.search(Query().command == self.name)

        if command_permission:
            return user in command_permission[-1]["permitted_users"]

        return False

    def permitted_users(self):
        if command_permission := self.table.search(Query().command == self.name):
            return command_permission[-1]["permitted_users"]
        else:
            return []

    def allow_user(self, target_user):
        if not self.skip_validation:
            if target_user not in WelcomeCommittee.fetch_present_users():
                raise ValueError(f"Not a valid user: {target_user}")

        command_permission = self.table.search(Query().command == self.name)
        print(
            f"\n\nAudioCommand#allow_user @{target_user} command_permission: {command_permission}"
        )

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

                self.table.update(add_permitted_users(), Query().command == self.name)

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
            self.table.insert(command_permission.__dict__)
            message = (
                f"User @{target_user} created new permissions for command: {self.name}"
            )
            send_twitch_msg(f"New CommandPermission created: {self.name}")

        return message

    # def _validate_user(self, user):
    #     if self.skip_validation:
    #         print("Skipping Validation for adding user permissions")
    #         return True
    #     user_eligible_for_permissions = (
    #         # user not in STREAM_LORDS
    #         user in WelcomeCommittee.fetch_present_users()
    #         and self.command not in SoundeffectsLibrary.fetch_theme_songs()
    #     )
    #     if not user_eligible_for_permissions:
    #         print("This user is not eligible for permissions")
    #     return user_eligible_for_permissions
