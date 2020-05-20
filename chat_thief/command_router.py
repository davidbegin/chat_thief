from typing import Dict, List, Optional
import logging
import os
import random

from chat_thief.prize_dropper import random_user as find_random_user

from chat_thief.routers.basic_info_router import BasicInfoRouter
from chat_thief.routers.feedback_router import FeedbackRouter
from chat_thief.routers.moderator_router import ModeratorRouter
from chat_thief.routers.cube_casino_router import CubeCasinoRouter
from chat_thief.routers.revolution_router import RevolutionRouter
from chat_thief.routers.user_soundeffect_router import UserSoundeffectRouter

from chat_thief.chat_parsers.perms_parser import PermsParser
from chat_thief.chat_parsers.props_parser import PropsParser
from chat_thief.chat_parsers.command_parser import CommandParser as ParseTime
from chat_thief.commands.command_giver import CommandGiver
from chat_thief.commands.command_sharer import CommandSharer
from chat_thief.commands.street_cred_transfer import StreetCredTransfer

from chat_thief.models.command import Command
from chat_thief.models.issue import Issue
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.models.user import User
from chat_thief.models.vote import Vote

from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.config.log import error, success, warning
from chat_thief.irc_msg import IrcMsg
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.config.commands_config import OBS_COMMANDS


BLACKLISTED_LOG_USERS = ["beginbotbot", "beginbot", "nightbot"]

HELP_COMMANDS = {
    "me": "Info about yourself",
    "buy": "!buy COMMAND or !buy random - Buy a Command with Cool Points",
    "love": "!love USER COMMAND - Show support for a command (Unmutes if theres Haters)",
    "hate": "!hate USER COMMAND - Vote to silence a command",
    "steal": "!steal COMMAND USER - steal a command from someone elses, cost Cool Points",
    "share": "!share COMMAND USER - share access to a command",
    "transfer": "!transfer COMMAND USER - transfer command to someone, costs no cool points",
    "props": "!props @beginbot (AMOUNT_OF_STREET_CRED) - Give you street cred to beginbot",
    "perms": "!perms !clap OR !perms @beginbot - See who is allowed to use the !clap command",
    "donate": "!donate give away all your commands to random users",
    "issue": "!issue Description of a Bug - A bug you found you want Beginbot to look at",
    "most_popular": "!most_popular - Shows the most coveted commands",
    "coup": "trigger either a revolution or a crushing or the rebellion based on !vote - if you don't have enough Cool Points to afford to trigger a coup, you will be stripped of all your Street Cred and Cool Points",
    "soundeffect": "!soundeffect YOUTUBE-ID YOUR_USERNAME 00:01 00:05 - Must be less than 5 second",
    "vote": "!vote (peace|revolution) - Where you stand when a coup happens.  Should all sounds be redistributed, or should the trouble makes lose their sounds and the rich get richer",
}

# This is only used for aliases
# so we might to respect that
# and then build out the list
COMMANDS = {
    "give": {
        "aliases": ["transfer", "give"],
        # "help": "!transfer COMMAND USER - transfer command to someone, costs no cool points",
    }
}

ROUTERS = [
    ModeratorRouter,
    BasicInfoRouter,
    FeedbackRouter,
    CubeCasinoRouter,
    RevolutionRouter,
    UserSoundeffectRouter,
]


class CommandRouter:
    def __init__(self, irc_msg: List[str], logger: logging.Logger) -> None:
        self._logger = logger
        self.irc_msg = IrcMsg(irc_msg)
        self.user = self.irc_msg.user
        self.msg = self.irc_msg.msg
        self.command = self.irc_msg.command
        self.args = self.irc_msg.args

    def build_response(self) -> Optional[str]:
        if self.user == "nightbot":
            return

        if self.user not in BLACKLISTED_LOG_USERS:
            self._logger.info(f"{self.user}: {self.msg}")
            WelcomeCommittee().welcome_new_users(self.user)

        success(f"\n{self.user}: {self.msg}")

        for Router in ROUTERS:
            if result := Router(self.user, self.command, self.args).route():
                return result

        return self._process_command()

    def _process_command(self):
        if self.command == "help":
            if len(self.args) > 0:
                command = self.args[0]
                if command.startswith("!"):
                    command = command[1:]
                return HELP_COMMANDS[command]
            else:
                options = " ".join([f"!{command}" for command in HELP_COMMANDS.keys()])
                return f"Call !help with a specfic command for more details: {options}"

        # ------------------
        # OBS or Soundeffect
        # ------------------

        if self.command in OBS_COMMANDS and self.user in STREAM_LORDS:
            print(f"executing OBS Command: {self.command}")
            return os.system(f"so {self.command}")

        if self.command:
            PlaySoundeffectRequest(user=self.user, command=self.command).save()
