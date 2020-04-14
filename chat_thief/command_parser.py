from typing import Dict, List, Optional
import logging
import os
from pathlib import Path
import subprocess
import traceback

from tinydb import TinyDB, Query

from chat_thief.obs import OBS_COMMANDS
from chat_thief.irc import send_twitch_msg
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.command_permissions import CommandPermissionCenter
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.audio_command_center import AudioCommandCenter

from chat_thief.commands.shoutout import shoutout
from chat_thief.prize_dropper import drop_soundeffect

from chat_thief.irc_msg import IrcMsg


# Separate out adding sound effects
class CommandParser:
    # TODO: Add Default Logger
    def __init__(self, irc_msg: List[str], logger: logging.Logger) -> None:
        self._logger = logger
        self.irc_msg = IrcMsg(irc_msg)
        self.user = self.irc_msg.user
        self.msg = self.irc_msg.msg
        self.command = self.irc_msg.command

        self.command_permission_center = CommandPermissionCenter()

    def build_response(self) -> Optional[str]:
        self._logger.info(f"{self.user}: {self.msg}")
        # self.audio_command_center.welcome_new_users()

        if self.irc_msg.is_command():
            command = self.msg[1:].split()[0]
            msg = self.msg.split()[0].lower()
            print(f"User: {self.user} | Command: {command}")

            if self.command == "dropeffect" and self.user in STREAM_LORDS:
                return drop_soundeffect()

            if self.command == "perms":
                return self.command_permission_center.fetch_command_permissions(
                    self.command
                )

            if self.command == "add_perm":
                return self.command_permission_center.add_perm(self.command)

            if self.command == "so":
                return shoutout(self.msg)

            if self.command == "whitelist":
                return " ".join(CommandPermissionCenter.fetch_whitelisted_users())

            if self.command == "streamlords":
                return " ".join(STREAM_LORDS)

            if self.command == "requests":
                return handle_user_requests()

            if self.command == "soundeffect":
                return AudioCommandCenter(self.irc_msg).add_command()

            self._try_anything()

        def _try_anything(self):
            # This is back to free mode
            # if self.user in fetch_whitelisted_users():
            #     self.try_soundeffect(command, msg)
            if self.user in self.command_permission_center.fetch_command_permissions(
                self.command
            ):
                self.try_soundeffect()
            else:
                print("hey you can't do that!")

    def try_soundeffect(self) -> None:
        if self.command in OBS_COMMANDS:
            print(f"executing OBS Command: {self.command}")
            os.system(f"so {self.command}")
        elif self.command in SoundeffectsLibrary.fetch_soundeffect_names():
            allowed_users = CommandPermissionCenter().fetch_command_permissions(
                self.command
            )
            if self.user in allowed_users:
                AudioCommandCenter(self.irc_msg).play_audio_command()
            else:
                print(f"\n{self.user} is NOT allowed {self.command}")
