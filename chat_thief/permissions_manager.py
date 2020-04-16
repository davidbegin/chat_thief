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
        db_location="db/soundeffects.json",
        skip_validation=False,
    ):
        self.user = user
        self.command = command
        self.args = args
        self.table = _command_permissions_table(db_location)
        self.skip_validation = skip_validation

    def add_perm(self):
        audio = AudioCommand(self.args[0])
        if self.user in STREAM_GODS:
            return self._add_permission()
        else:
            if self.args[1] in audio.permitted_users():
                return self._add_permission()
            else:
                print(f"{self.user} cannot add permissions")

    def _add_permission(self):
        if len(self.args) < 2:
            print("you need more args!")
            return

        return AudioCommand(self.args[0]).allow_user(self.args[1])
