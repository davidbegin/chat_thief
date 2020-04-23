from pathlib import Path
from typing import Dict, List, Optional
import logging
import os
import subprocess
import traceback

from chat_thief.audio_command import AudioCommand
from chat_thief.chat_logs import ChatLogs
from chat_thief.chat_parsers.soundeffect_request_parser import SoundeffectRequestParser
from chat_thief.chat_parsers.transfer_request_parser import TransferRequestParser

from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.commands.command_giver import CommandGiver
from chat_thief.commands.command_sharer import CommandSharer
from chat_thief.commands.cube_casino import CubeCasino
from chat_thief.commands.leaderboard import leaderboard, loserboard
from chat_thief.commands.shoutout import shoutout
from chat_thief.commands.street_cred_transfer import StreetCredTransfer
from chat_thief.commands.user_requests import handle_user_requests
from chat_thief.irc import send_twitch_msg
from chat_thief.irc_msg import IrcMsg
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.permissions_manager import PermissionsManager
from chat_thief.prize_dropper import drop_soundeffect, dropreward
from chat_thief.revolution import Revolution
from chat_thief.user import User

from chat_thief.commands.approve_all_requests import ApproveAllRequests

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

OBS_COMMANDS = [
    "wyp",
    "idk",
    "jdi",
    "brb",
    "i_hate_that_thing",
    "i_like_that_thing",
]

HELP_MENU = [
    "!me - Info about your self",
    "!share COMMAND USER_TO_GIVE_PERMS - share someone else access to a command you have access to",
    "!transfer COMMAND USER_TO_GIVE_PERMS - transfer your command to someone else, costs no cool points, but you lose access",
    "!props beginbot (OPTIONAL_AMOUNT_OF_STREET_CRED) - Give you street cred to beginbot",
    "!perms clap - See who is allowed to use the !clap command",
    "!perms beginbot - See what commands beginbot has access to",
    "!leaderboard - See what users have the most commands",
    "!soundeffect YOUTUBE-ID YOUR_USERNAME 00:01 00:05 - Must be less than 5 second",
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

            if self.command == "color" and self.user in STREAM_GODS:
                subprocess.call(["/usr/bin/wal", "--theme", "random_dark"])

            if self.command == "revolution":
                return Revolution(self.user).incite()

            if self.command == "paperup":
                if self.user in STREAM_GODS:
                    return User(self.args[0]).paperup()

            if self.command in ["me"]:
                perms = PermissionsFetcher.fetch_permissions(
                    user=self.user, args=self.args,
                )
                stats = User(self.user).stats()
                if perms:
                    return [stats, perms]
                else:
                    return stats

            if self.command in ["permissions", "permission", "perms", "perm"]:
                perms = PermissionsFetcher.fetch_permissions(
                    user=self.user, args=self.args,
                )
                if perms:
                    return perms
                else:
                    return f"We found no permissions for {self.user} {self.args}"

            if self.command == "peasants":
                return ChatLogs().recent_stream_peasants()

            if self.command == "loserboard":
                from chat_thief.commands.leaderboard import loserboard

                return loserboard()

            # Drop randomeffect for new users
            # Weight For Powers

            if self.command in ["economy"]:
                # Print total Number of Cool Points
                cool_points = User(self.user).total_cool_points()
                return f"Total Cool Points in Market: {cool_points}"

            if self.command in ["buy"]:
                return User(self.user).buy(self.args)

            if self.command == "dropeffect" and self.user in STREAM_GODS:
                return drop_soundeffect(self.user, self.args)

            if self.command == "dropreward" and self.user in STREAM_GODS:
                return dropreward()

            if self.command in [
                "give",
                "transfer",
            ]:
                parser = TransferRequestParser(self.user, self.args).parse()

                return CommandGiver(
                    parser.transferer, parser.target_command, parser.target_user
                ).give()

            if self.command in [
                "share",
                "add_perm",
                "add_perms",
                "share_perm",
                "share_perms",
            ]:
                parser = TransferRequestParser(self.user, self.args).parse()
                return CommandSharer(
                    self.user, parser.target_command, parser.target_user
                ).share()

            if self.command in [
                "props",
                "bigups",
                "endorse",
            ]:
                cool_person = self.args[0]
                if cool_person.startswith("@"):
                    cool_person = cool_person[1:]
                cool_person = cool_person.lower()

                if cool_person == "random":
                    from chat_thief.prize_dropper import random_user

                    cool_person = random_user()

                if len(self.args) > 1 and int(self.args[1]) > 0:
                    amount = int(self.args[1])
                else:
                    amount = 1

                if amount < 1:
                    raise ValueError(f"Invalid Amount: {amount}")
                print(f"\n{self.user} Attempting to give {amount} Cool Points")

                return StreetCredTransfer(
                    user=self.user, cool_person=cool_person, amount=amount
                ).transfer()

            if self.command == "help":
                return HELP_MENU

            if self.command == "users":
                return WelcomeFile.present_users()

            if self.command == "all_bets":
                return CubeCasino(self.user, self.args).all_bets()

            if self.command == "bet":
                return CubeCasino(self.user, self.args).bet()

            if self.command == "new_cube" and self.user == "beginbotbot":
                return CubeCasino(self.user, self.args).purge()

            if self.command == "cubed" and self.user in ["beginbot", "beginbotbot"]:
                cube_time = int(self.args[0])
                return CubeCasino(self.user, self.args).closet_result(cube_time)

            if self.command == "so":
                return shoutout(self.msg)

            if self.command == "whitelist":
                return " ".join(PermissionsFetcher.fetch_whitelisted_users())

            if self.command == "streamlords":
                return " ".join(STREAM_LORDS)

            if self.command == "streamgods":
                return " ".join(STREAM_GODS)

            if self.command == "requests":
                return handle_user_requests()

            if (
                self.command in ["approve", "approve_all_requests"]
                and self.user in STREAM_LORDS
            ):
                request_user = self.args[0].lower()
                return ApproveAllRequests.approve(self.user, request_user)

            if self.command == "soundeffect":
                sfx_request = SoundeffectRequestParser(self.user, self.irc_msg.args)

                return SoundeffectRequest(
                    user=self.user,
                    youtube_id=sfx_request.youtube_id,
                    command=sfx_request.command,
                    start_time=sfx_request.start_time,
                    end_time=sfx_request.end_time,
                ).save()

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
