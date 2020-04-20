from pathlib import Path
from typing import Dict, List, Optional
import logging
import os
import subprocess
import traceback

from chat_thief.audio_command import AudioCommand
from chat_thief.audio_command_center import AudioCommandCenter
from chat_thief.chat_logs import ChatLogs
from chat_thief.command_permissions import CommandPermissionCenter
from chat_thief.commands.leaderboard import leaderboard, loserboard
from chat_thief.commands.shoutout import shoutout
from chat_thief.commands.street_cred_transfer import StreetCredTransfer
from chat_thief.commands.user_requests import handle_user_requests
from chat_thief.irc import send_twitch_msg
from chat_thief.irc_msg import IrcMsg
from chat_thief.obs import OBS_COMMANDS
from chat_thief.permissions_manager import PermissionsManager
from chat_thief.prize_dropper import drop_soundeffect, dropreward
from chat_thief.new_models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.user import User

from chat_thief.request_saver import RequestSaver
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.welcome_file import WelcomeFile

BLACKLISTED_LOG_USERS = [
    "beginbotbot",
    "beginbot",
    "nightbot",
]

HELP_MENU = [
    "!me - Info about your self",
    "!perms - Check what soundeffects you have access to",
    "!soundeffect YOUTUBE-ID YOUR_USERNAME 00:01 00:05 - Must be less than 5 second",
    "!add_perm COMMAND USER_TO_GIVE_PERMS - give someone else access to a command you have access to",
    "!perms clap - See who is allowed to use the !clap command",
    "!perms beginbot - See what commands beginbot has access to",
    "!props beginbot (OPTIONAL_AMOUNT_OF_STREET_CRED) - Give you street cred to beginbot",
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
        if self.user not in BLACKLISTED_LOG_USERS:
            self._logger.info(f"{self.user}: {self.msg}")
            WelcomeCommittee(self.user).welcome_new_users()
        else:
            print(f"{self.user}: {self.msg}")

        if self.irc_msg.is_command():
            command = self.msg[1:].split()[0]
            msg = self.msg.split()[0].lower()
            print(f"User: {self.user} | Command: {command}")

            if self.command in ["leaderboard", "forbes"]:
                from chat_thief.commands.leaderboard import leaderboard

                return leaderboard()

            if self.command == "me":
                return User(self.user).stats()

            if self.command == "peasants":
                return ChatLogs().recent_stream_peasants()

            if self.command == "loserboard":
                from chat_thief.commands.leaderboard import loserboard

                return loserboard()

            # Drop randomeffect for new users
            # Weight For Powers

            if self.command in ["buy"]:
                return User(self.user).buy(self.args)

            if self.command == "dropeffect" and self.user in STREAM_GODS:
                return drop_soundeffect(self.user, self.args)

            if self.command == "dropreward" and self.user in STREAM_GODS:
                return dropreward()

            if self.command in ["permissions", "permission", "perms", "perm"]:
                perms = CommandPermissionCenter.fetch_permissions(
                    user=self.user, args=self.args,
                )
                return " ".join([f"!{command}" for command in perms])

            if self.command in [
                "give",
                "share",
                "add_perm",
                "add_perms",
                "share_perm",
                "share_perms",
            ]:
                return PermissionsManager(
                    user=self.user, command=self.command, args=self.args,
                ).add_perm()

            if self.command in [
                "props",
                "bigups",
                "endorse",
            ]:
                cool_person = self.args[0]
                if len(self.args) > 1:
                    amount = int(self.args[1])
                else:
                    amount = 1

                return StreetCredTransfer(
                    user=self.user, cool_person=cool_person, amount=amount
                ).transfer()

            if self.command == "help":
                return HELP_MENU

            if self.command == "users":
                return WelcomeFile.present_users()

            if self.command == "so":
                return shoutout(self.msg)

            if self.command == "whitelist":
                return " ".join(CommandPermissionCenter.fetch_whitelisted_users())

            if self.command == "streamlords":
                return " ".join(STREAM_LORDS)

            if self.command == "streamgods":
                return " ".join(STREAM_GODS)

            if self.command == "requests":
                return handle_user_requests()

            # soundeffects saver bot
            # soundeffects player bot
            # This should save somewhere
            if self.command == "soundeffect":
                return AudioCommandCenter(self.irc_msg).add_command()

            self.try_soundeffect()

    # This should Save somewhere
    # Set a 5 Minute Party Mode
    # if self.user in fetch_whitelisted_users():
    #     self.try_soundeffect(command, msg)
    def try_soundeffect(self) -> None:
        if self.command in OBS_COMMANDS and self.user in STREAM_LORDS:
            print(f"executing OBS Command: {self.command}")
            os.system(f"so {self.command}")
            return

        PlaySoundeffectRequest(user=self.user, command=self.command).save()
