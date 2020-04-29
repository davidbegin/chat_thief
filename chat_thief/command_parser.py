import random
from pathlib import Path
from typing import Dict, List, Optional
import logging
import os
import subprocess
import traceback

from chat_thief.chat_logs import ChatLogs

from chat_thief.chat_parsers.soundeffect_request_parser import SoundeffectRequestParser
from chat_thief.chat_parsers.perms_parser import PermsParser
from chat_thief.chat_parsers.props_parser import PropsParser
from chat_thief.models.vote import Vote

from chat_thief.commands.approve_all_requests import ApproveAllRequests
from chat_thief.commands.command_sharer import CommandSharer
from chat_thief.commands.cube_casino import CubeCasino
from chat_thief.commands.leaderboard import leaderboard, loserboard
from chat_thief.commands.shoutout import shoutout
from chat_thief.commands.street_cred_transfer import StreetCredTransfer
from chat_thief.commands.user_requests import handle_user_requests
from chat_thief.commands.revolution import Revolution


from chat_thief.irc_msg import IrcMsg

from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.models.user import User

from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.permissions_manager import PermissionsManager

from chat_thief.prize_dropper import drop_soundeffect, dropreward, random_soundeffect
from chat_thief.request_saver import RequestSaver
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.welcome_committee import WelcomeCommittee

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
            WelcomeCommittee().welcome_new_users(self.user)
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
                return subprocess.call(["/usr/bin/wal", "--theme", "random_dark"])

            if self.command == "coup" and self.user == "beginbotbot":
                threshold = int(User(self.user).total_users() / 8)
                # threshold = int(User(self.user).total_users() / 2)
                result = Vote(user=self.user).have_tables_turned(threshold)
                print(f"The Result of have_tables_turned: {result}")

                if result in ["peace", "revolution"]:
                    # return f"{result} COMING SOON"
                    return Revolution(tide=result).turn_the_tides()
                else:
                    return f"The Will of the People have not chosen: {threshold} votes must be cast"
                pass

            if self.command == "revolution":
                return Vote(user=self.user).vote("revolution")

            if self.command == "peace":
                return Vote(user=self.user).vote("peace")

            if self.command == "facts" and self.user in STREAM_GODS:
                from chat_thief.economist.facts import Facts

                Facts().available_sounds()

            if self.command == "paperup":
                if self.user in STREAM_GODS:
                    return User(self.args[0]).paperup()
                else:
                    return

            if self.command in ["me"]:
                parser = PermsParser(user=self.user, args=self.args).parse()
                perms = PermissionsFetcher.fetch_permissions(
                    user=self.user,
                    target_user=parser.target_user,
                    target_command=parser.target_command,
                )
                stats = User(self.user).stats()
                if perms:
                    return [stats, perms]
                else:
                    return stats

            if self.command in ["permissions", "permission", "perms", "perm"]:
                parser = PermsParser(user=self.user, args=self.args).parse()

                perms = PermissionsFetcher.fetch_permissions(
                    user=self.user,
                    target_user=parser.target_user,
                    target_command=parser.target_command,
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

            if self.command in ["economy"]:
                cool_points = User(self.user).total_cool_points()
                return f"Total Cool Points in Market: {cool_points}"

            if self.command in ["buy"]:
                parser = PermsParser(
                    user=self.user, args=self.args, random_command=True, perm_type="buy"
                ).parse()
                return User(self.user).buy(parser.target_command)

            # These Need Chat Parsers
            if self.command == "dropeffect" and self.user in STREAM_GODS:
                return drop_soundeffect(self.user, self.args)

            if self.command == "dropreward" and self.user in STREAM_GODS:
                return dropreward()

            if self.command in [
                "give",
                "transfer",
            ]:
                parser = PermsParser(
                    user=self.user,
                    args=self.args,
                    random_command=True,
                    random_user=True,
                ).parse()

                return PermissionsManager(
                    user=self.user,
                    command=self.command,
                    target_command=parser.target_command,
                    target_user=parser.target_user,
                ).swap_perm()

            if self.command in [
                "share",
                "clone",
                "add_perm",
                "add_perms",
                "share_perm",
                "share_perms",
            ]:
                parser = PermsParser(
                    user=self.user, args=self.args, random_user=True
                ).parse()
                return CommandSharer(
                    self.user, parser.target_command, parser.target_user
                ).share()

            if self.command in [
                "props",
                "bigups",
                "endorse",
            ]:
                parser = PropsParser(user=self.user, args=self.args).parse()
                if parser.target_user == "random":
                    from chat_thief.prize_dropper import random_user

                    parser.target_user = random_user(blacklisted_users=[self.user])
                return StreetCredTransfer(
                    user=self.user, cool_person=parser.target_user, amount=parser.amount
                ).transfer()

            if self.command == "help":
                return HELP_MENU

            if self.command == "users":
                return WelcomeCommittee().present_users()

            if self.command in ["all_bets", "all_bet", "bets"]:
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
