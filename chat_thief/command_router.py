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
from chat_thief.models.user import User
from chat_thief.prize_dropper import drop_effect

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

        if self.command == "whylua":
            os.system(f"scene codin_and_teej")

        pack_config = {
            "teej_pack" : [],
            "dean_pack" : [],
            "erik_pack" : [],
            "vim_pack" : [],
            "pokemon_pack" : [],
            "sandstorm_pack" : [],
            "linux_pack" : [],
            "eightbit_pack" : [ "8bitmack", "8bitymca", "8bitmackintro",
                "8bitsk8erboi", "8bitmacarena", "8bitrickandmorty", "8bitimperial",
                "8bitfriday", "8bitghostbusters1", "8bitghostbuster2",
                "8bitfatbottomedgirls", "8bittoto", "8bitbitesthedust",
                "8bitchampions", "8bitbohemian", "8bitbagpipes", "8bitwreckingball",
                "8bitzelda", "8bitonemoretime", "8bitabout", "8bitblue",
                "8bithammer", "8bitafrica", "8bitrugrats", "8bitroll",
                "8bitparadise", "8bitrangers", "8bitcalifornialove" ],
            "silicon_valley_pack" : [],
            "gaming_pack" : [],
            "begin_pack" : [ "itsmedavid", "penisinspected", "bestsound",
                "beginsing", "beginvimeyes", "crack" ],
            "yacht_pack" : [],
            "luke_pack" : [ "gcc", "alpine", "xoomers", "inspiredme", "i3", "i3v2", "python" ],
            "wesley_willis_pack" : [],
            "art_matt_pack" : ["thisiscoke", "easyartmatt", "zenofartmatt", "moremore", "thisslaps"],
            "shannon_pack" : [],
            "meme_pack" : [],
            "i3_pack" : [],
            "prime_pack" : [ "primetrollsbegin", "primebegin", "primeslam", "primeagen", "primeagenpity", "begin_v_prime", "nevervim", ]
        }

        if self.command in pack_config["prime_pack"]:
            os.system(f"scene primetime")

        if self.command == "droppack" and self.user in STREAM_GODS and self.args[0] in pack_config.keys():
            sounds = pack_config[ self.args[0] ]
            for sound in sounds:
                drop_effect(parser.target_user, sound)
            return f"Dropping the {self.args[0]} Pack for {parser.target_user}"

        if self.command in OBS_COMMANDS and self.user in STREAM_LORDS:
            print(f"executing OBS Command: {self.command}")
            return os.system(f"so {self.command}")

        if self.command == "trollbegin" and User(self.user).mana() > 0:
            User(self.user).kill()
            pause = 1
            if parser.amount > 10:
                return "Trolling is the Art of Sublety"

            for _ in range(0, parser.amount):
                spin_begin(pause / parser.amount)
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
