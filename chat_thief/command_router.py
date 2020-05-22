from typing import Dict, List, Optional
import logging
import traceback
import os

from chat_thief.config.commands_config import OBS_COMMANDS
from chat_thief.config.log import error, success, warning
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.irc_msg import IrcMsg
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.routers.basic_info_router import BasicInfoRouter
from chat_thief.routers.beginworld_help_router import BeginworldHelpRouter
from chat_thief.routers.cube_casino_router import CubeCasinoRouter
from chat_thief.routers.feedback_router import FeedbackRouter
from chat_thief.routers.moderator_router import ModeratorRouter
from chat_thief.routers.revolution_router import RevolutionRouter
from chat_thief.routers.community_router import CommunityRouter
from chat_thief.routers.user_soundeffect_router import UserSoundeffectRouter
from chat_thief.welcome_committee import WelcomeCommittee

BLACKLISTED_LOG_USERS = ["beginbotbot", "beginbot", "nightbot"]

ROUTERS = [
    ModeratorRouter,
    BasicInfoRouter,
    FeedbackRouter,
    CubeCasinoRouter,
    RevolutionRouter,
    UserSoundeffectRouter,
    BeginworldHelpRouter,
    CommunityRouter,
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
            try:
                if result := Router(self.user, self.command, self.args).route():
                    return result
            except Exception as e:
                traceback.print_exc()
                # raise e

        if self.user in STREAM_GODS:
            # print("Oh boy we got a STREAM GOD here hmmm")
            # if self.command == "curb_your_begin":
            #     return BreakingNews(" ".join(self.irc_msg.args), category="curb").save()

            if self.command == "iasip":
                return BreakingNews(
                    " ".join(self.irc_msg.args), category="iasip"
                ).save()

        if self.command in OBS_COMMANDS and self.user in STREAM_LORDS:
            print(f"executing OBS Command: {self.command}")
            return os.system(f"so {self.command}")

        if self.command:
            PlaySoundeffectRequest(user=self.user, command=self.command).save()
