from pathlib import Path
import traceback

from tinydb import TinyDB, Query

from chat_thief.models import SoundEffect, CommandPermission
from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.irc import send_twitch_msg
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.audio_command import AudioCommand
from chat_thief.models import _command_permissions_table, DEFAULT_DB_LOCATION

from tinydb import Query


class PermissionsManager:
    def __init__(
        self,
        user,
        command=None,
        args=[],
        db_location=DEFAULT_DB_LOCATION,
        skip_validation=False,
    ):
        self.user = user
        self.command = command

        if len(args) < 2:
            print("you need more args: command user!")
            raise ArgumentError

        self.target_command = args[0]
        self.target_user = args[1]

        self.table = _command_permissions_table(db_location)
        self.skip_validation = skip_validation
        self.audio_command = AudioCommand(self.target_command, db_location=db_location)

    def add_perm(self):
        permitted_users = self.audio_command.permitted_users()

        if self.user in STREAM_GODS:
            return self.audio_command.allow_user(self.target_user)
        else:
            print(f"Permitted Users For: {self.target_command} {permitted_users}")

            if self.user in permitted_users:
                return self.audio_command.allow_user(self.target_user)
            else:
                print(f"{self.user} cannot add permissions")
