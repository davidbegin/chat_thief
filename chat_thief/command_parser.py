from pathlib import Path
from typing import Dict, List, Optional
import logging
import os
import subprocess
import traceback

from chat_thief.audio_command_center import AudioCommandCenter
from chat_thief.command_permissions import CommandPermissionCenter
from chat_thief.permissions_manager import PermissionsManager
from chat_thief.commands.shoutout import shoutout
from chat_thief.irc import send_twitch_msg
from chat_thief.irc_msg import IrcMsg
from chat_thief.obs import OBS_COMMANDS
from chat_thief.prize_dropper import drop_soundeffect
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.audio_command import AudioCommand

from chat_thief.request_saver import RequestSaver
from chat_thief.commands.user_requests import handle_user_requests
from chat_thief.commands.leaderboard import leaderboard

HELP_MENU = [
    "!perms - Check what soundeffects you have access to",
    "!soundeffect YOUTUBE-ID YOUR_USERNAME 00:01 00:05 - Must be less than 5 second",
    "!add_perm COMMAND USER_TO_GIVE_PERMS - give someone else access to a command you have access to",
    "!perms clap - See who is allowed to use the !clap command",
    "!perms beginbot - See what commands beginbot has access to",
    "!leaderboard - See what users have the most commands",
]


class CommandParser:
    def __init__(self, irc_msg: List[str], logger: logging.Logger) -> None:
        self._logger = logger
        self.irc_msg = IrcMsg(irc_msg)

        self.user = self.irc_msg.user
        self.msg = self.irc_msg.msg
        self.command = self.irc_msg.command
        self.args = self.irc_msg.args

    def build_response(self) -> Optional[str]:
        self._logger.info(f"{self.user}: {self.msg}")
        WelcomeCommittee(self.user).welcome_new_users()

        if self.irc_msg.is_command():
            command = self.msg[1:].split()[0]
            msg = self.msg.split()[0].lower()
            print(f"User: {self.user} | Command: {command}")

            if self.command == "leaderboard":
                return leaderboard()

            if self.command == "dropeffect" and self.user in STREAM_LORDS:
                return drop_soundeffect(self.user, self.args)

            if self.command in ["permissions", "permission", "perms", "perm"]:
                return CommandPermissionCenter.fetch_permissions(
                    user=self.user, args=self.args,
                )

            if self.command in ["add_perm", "add_perms", "share_perm", "share_perms"]:
                return PermissionsManager(
                    user=self.user, command=self.command, args=self.args,
                ).add_perm()

            if self.command == "help":
                return HELP_MENU

            if self.command == "users":
                return WelcomeCommittee.fetch_present_users()

            if self.command == "so":
                return shoutout(self.msg)

            if self.command == "whitelist":
                return " ".join(CommandPermissionCenter.fetch_whitelisted_users())

            if self.command == "streamlords":
                return " ".join(STREAM_LORDS)

            if self.command == "requests":
                handle_user_requests()
            if self.command == "soundeffect":
                return AudioCommandCenter(self.irc_msg).add_command()

            self.try_soundeffect()

    # This is back to free mode
    # if self.user in fetch_whitelisted_users():
    #     self.try_soundeffect(command, msg)
    def try_soundeffect(self) -> None:
        if self.command in OBS_COMMANDS and self.user in STREAM_LORDS:
            print(f"executing OBS Command: {self.command}")
            os.system(f"so {self.command}")
            return

        audio_command = AudioCommand(self.command)

        if audio_command.allowed_to_play(self.user):
            audio_command.play_sample()
        else:
            print(f"\n{self.user} is NOT allowed {self.command}")
