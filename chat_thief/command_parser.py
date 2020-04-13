from typing import Dict, List, Optional
import logging
import random
import os
import random
from pathlib import Path
from dataclasses import dataclass
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
from chat_thief.audio_command_center import (
    AudioCommandCenter
)

from chat_thief.commands.shoutout import shoutout
from chat_thief.commands.user_requests import handle_user_requests


# Separate out adding sound effects
class CommandParser:
    # TODO: Add Default Logger
    def __init__(self, irc_msg: List[str], logger: logging.Logger) -> None:
        self._irc_msg = irc_msg
        self._logger = logger
        user_info, _, _, *raw_msg = self._irc_msg
        self.user = user_info.split("!")[0][1:]
        self.msg = self._msg_sanitizer(raw_msg)
        self.audio_command_center = AudioCommandCenter(user=self.user, msg=self.msg)
        self.command_permission_center = CommandPermissionCenter()

    # This belongs somwehre else
    def try_soundeffect(self, command, msg):
        if command in OBS_COMMANDS:
            print(f"executing OBS Command: {msg}")
            os.system(f"so {command}")
        elif command in SoundeffectsLibrary.fetch_soundeffect_names():
            self.audio_command_center.audio_command(command)

    def add_permission(self, command):
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

    def random_soundeffect(self):
        return random.sample(SoundeffectsLibrary.soundeffects_only(), 1)[0]

    # Not include STREAM LORDS
    def random_user(self):
        return random.sample(WelcomeCommittee.fetch_present_users(), 1)[0]

    def drop_soundeffect(self):
        user = self.random_user()
        soundeffect = self.random_soundeffect()
        soundeffect_name = soundeffect
        self.command_permission_center.add_permission_for_user(user, soundeffect_name)
        msg = f"@{user} now has access to Sound Effect: !{soundeffect_name}"
        return msg

    def build_response(self) -> Optional[str]:
        self._logger.info(f"{self.user}: {self.msg}")
        # self.audio_command_center.welcome_new_users()

        if self._is_command_msg():
            command = self.msg[1:].split()[0]
            msg = self.msg.split()[0].lower()
            print(f"User: {self.user} | Command: {command}")

            if msg == "!dropeffect":
                if self.user in STREAM_LORDS:
                    return self.drop_soundeffect()

            if msg == "!perms":
                _, command, *_ = self.msg.split(" ")
                return self.command_permission_center.fetch_command_permissions(command)

            if msg == "!add_perm":
                return self.add_permission(command)

            if msg == "!so":
                return shoutout(self.msg)

            if msg == "!whitelist":
                return " ".join(WelcomeCommittee.fetch_whitelisted_users())

            if msg == "!streamlords":
                return " ".join(STREAM_LORDS)

            if msg == "!requests":
                return handle_user_requests()

            if msg == "!soundeffect":
                return self.audio_command_center.add_command()

            # We need to start blocking if not allowed
            if self.user in self.command_permission_center.fetch_command_permissions(
                command
            ):
                self.try_soundeffect(command, msg)
            else:
                print("hey you can't do that!")

            # if self.user in fetch_whitelisted_users():
            #     self.try_soundeffect(command, msg)

        return None

    def _msg_sanitizer(self, msg: List[str]) -> str:
        first, *rest = msg
        return f"{first[1:]} {' '.join(rest)}"

    def _is_command_msg(self) -> bool:
        return self.msg[0] == "!" and self.msg[1] != "!"
