from typing import Dict, List, Optional
import logging
import traceback
import os
import time

from chat_thief.config.commands_config import OBS_COMMANDS
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.config.log import error, success, warning
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.irc_msg import IrcMsg
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.models.user_event import UserEvent

from chat_thief.routers import *

from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.new_commands.result import Result

BLACKLISTED_LOG_USERS = ["beginbotbot", "beginbot", "nightbot"]
# BLACKLISTED_LOG_USERS = []

ROUTERS = [
    EconomyRouter,
    BasicInfoRouter,
    BeginworldHelpRouter,
    BotSurvivorRouter,
    CommunityRouter,
    FeedbackRouter,
    ModeratorRouter,
    NewCubeCasinoRouter,
    PokemonCasinoRouter,
    RevolutionRouter,
    UserCodeRouter,
    VotingBoothRouter,
]

def spin_begin(pause):
    SCENES = [
        "TopRight",
        "TopLeft",
        "BottomLeft",
        "Giger",
        "BottomLeft",
        "hottub",
        "codin",
    ]

    for scene in SCENES:
        os.system(f"scene {scene}")
        time.sleep(pause)

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

        if self.user in STREAM_GODS:
            print(f"Oh Look we got a Stream God over here: {self.user}")
            if self.command == "curb_your_begin":
                return BreakingNews(" ".join(self.irc_msg.args), category="curb").save()

            if self.command in ["iasip", "alwayssunny"]:
                BreakingNews(" ".join(self.irc_msg.args), category="iasip").save()
                return

        parser = CommandParser(
            user=self.user, command=self.command, args=self.args
        ).parse()

        for Router in ROUTERS:
            try:
                if result := Router(self.user, self.command, self.args, parser).route():

                    # TODO: Sort out this Result Concept Better
                    if isinstance(result, Result):
                        # TODO: Update This
                        UserEvent(
                            user=self.irc_msg.user,
                            command=self.irc_msg.command,
                            msg=self.irc_msg.msg,
                            result=[],
                            # result=result,
                        ).save()
                    else:
                        UserEvent(
                            user=self.irc_msg.user,
                            command=self.irc_msg.command,
                            msg=self.irc_msg.msg,
                            result=result,
                        ).save()

                    return result
            except Exception as e:
                traceback.print_exc()
                # raise e

        if self.command in OBS_COMMANDS and self.user in STREAM_LORDS:
            print(f"executing OBS Command: {self.command}")
            return os.system(f"so {self.command}")

        if self.command == "trollbegin" and self.user in STREAM_LORDS:
            pause = 1
            for _ in range(0, parser.amount):
                spin_begin(pause)
            return

        if self.command == "hottub" and self.user in STREAM_LORDS:
            return os.system("scene hottub")

        if self.command in SoundeffectsLibrary.fetch_soundeffect_names():
            if self.command:
                return PlaySoundeffectRequest(
                    user=self.user, command=self.command
                ).save()

        from pathlib import Path

        user_msgs_path = Path(__file__).parent.parent.joinpath("logs/user_msgs.log")
        if self.user not in BLACKLISTED_LOG_USERS:
            with open(user_msgs_path, "a") as log_file:
                log_file.write(f"{self.user}: {self.msg}\n")
