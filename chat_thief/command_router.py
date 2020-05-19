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

from chat_thief.chat_parsers.request_approver_parser import RequestApproverParser
from chat_thief.chat_parsers.perms_parser import PermsParser
from chat_thief.chat_parsers.props_parser import PropsParser
from chat_thief.chat_parsers.command_parser import CommandParser as ParseTime
from chat_thief.commands.airdrop import Airdrop
from chat_thief.commands.command_giver import CommandGiver
from chat_thief.commands.command_sharer import CommandSharer
from chat_thief.commands.command_stealer import CommandStealer
from chat_thief.commands.donator import Donator
from chat_thief.commands.leaderboard import leaderboard, loserboard
from chat_thief.commands.street_cred_transfer import StreetCredTransfer
from chat_thief.economist.facts import Facts

from chat_thief.models.command import Command
from chat_thief.models.issue import Issue
from chat_thief.models.play_soundeffect_request import PlaySoundeffectRequest
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.models.user import User
from chat_thief.models.vote import Vote

from chat_thief.chat_logs import ChatLogs
from chat_thief.config.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.config.log import error, success, warning
from chat_thief.irc_msg import IrcMsg
from chat_thief.irc import send_twitch_msg
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.prize_dropper import drop_soundeffect, dropreward
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


YOU_WERE_THE_CHOSEN = ["beginbot", "beginbotbot"]


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

        result = ModeratorRouter(self.user, self.command, self.args).route()
        if result:
            return result

        result = BasicInfoRouter(self.user, self.command, self.args).route()
        if result:
            return result

        result = FeedbackRouter(self.user, self.command, self.args).route()
        if result:
            return result

        result = CubeCasinoRouter(self.user, self.command, self.args).route()
        if result:
            return result

        result = RevolutionRouter(self.user, self.command, self.args).route()
        if result:
            return result

        return self._process_command()

    def _process_command(self):

        # -------------------------
        # No Random Command or User
        # -------------------------

        if self.command in ["me"]:
            parser = PermsParser(user=self.user, args=self.args).parse()

            user_permissions = " ".join(
                [f"!{perm}" for perm in User(self.user).commands()]
            )
            stats = User(self.user).stats()
            if user_permissions:
                return f"{stats} | {user_permissions}"
            else:
                return stats

        # ------------
        # Takes a User
        # ------------

        if self.command == "donate":
            parser = PermsParser(user=self.user, args=self.args).parse()
            if parser.target_user:
                return Donator(self.user).donate(parser.target_user)
            else:
                return Donator(self.user).donate()

        # ---------------
        # Takes a Command
        # ---------------

        if self.command == "help":
            if len(self.args) > 0:
                command = self.args[0]
                if command.startswith("!"):
                    command = command[1:]
                return HELP_COMMANDS[command]
            else:
                options = " ".join([f"!{command}" for command in HELP_COMMANDS.keys()])
                return f"Call !help with a specfic command for more details: {options}"

        # ===============================================

        if self.command in ["dislike", "hate", "detract"]:
            parser = PermsParser(user=self.user, args=self.args).parse()

            if parser.target_command and not parser.target_user:
                result = SFXVote(parser.target_command).detract(self.user)
                return f"!{parser.target_command} supporters: {len(result['supporters'])} | detractors {len(result['detractors'])}"
            else:
                print("Doing Nothing")

        if self.command in ["support", "love", "like"]:
            parser = PermsParser(user=self.user, args=self.args).parse()

            if parser.target_command and not parser.target_user:
                result = SFXVote(parser.target_command).support(self.user)
                return f"!{parser.target_command} supporters: {len(result['supporters'])} | detractors {len(result['detractors'])}"

            if parser.target_user and not parser.target_command:
                if self.user == parser.target_user:
                    return f"You can love yourself in real life, but not in Beginworld @{self.user}"
                else:
                    User(self.user).set_ride_or_die(parser.target_user)
                    return f"@{self.user} Made @{parser.target_user} their Ride or Die"
            else:
                return None

        # This only works for soundeffects
        if self.command in ["permissions", "permission", "perms", "perm"]:
            parser = PermsParser(user=self.user, args=self.args).parse()

            if (
                len(self.args) > 0
                and not parser.target_command
                and not parser.target_user
            ):
                raise ValueError(
                    f"Could not find user or command: {' '.join(self.args)}"
                )
            return PermissionsFetcher.fetch_permissions(
                user=self.user,
                target_user=parser.target_user,
                target_command=parser.target_command,
            )

        # -----------
        # Random User
        # -----------

        if self.command in [
            "props",
            "bigups",
            "endorse",
        ]:
            parser = PropsParser(user=self.user, args=self.args).parse()
            if parser.target_user == "random" or not parser.target_user:
                parser.target_user = self.random_not_you_user()

            return StreetCredTransfer(
                user=self.user, cool_person=parser.target_user, amount=parser.amount
            ).transfer()

        if self.command in [
            "share",
            "clone",
            "add_perm",
            "add_perms",
            "share_perm",
            "share_perms",
        ]:
            parser = PermsParser(
                user=self.user, args=self.args, random_user=True, random_command=True
            ).parse()

            if parser.target_command == "random":
                commands = User(self.user).commands()
                parser.target_command = random.sample(commands, 1)[0]

            if parser.target_user == "random":
                parser.target_user = find_random_user(
                    blacklisted_users=Command(command).users()
                )

            if parser.target_user and parser.target_command:
                return CommandSharer(
                    self.user, parser.target_command, parser.target_user
                ).share()
            else:
                return f"Error Sharing - Command: {parser.target_command} | User: {parser.target_user}"

        # --------------
        # Random Command
        # --------------

        if self.command in ["buy"]:
            from chat_thief.commands.command_buyer import CommandBuyer

            parser = ParseTime(
                user=self.user,
                command=self.command,
                args=self.args,
                allow_random_sfx=True,
            ).parse()

            return CommandBuyer(user=self.user, target_sfx=parser.target_sfx).buy()

        # ------------------------------
        # Random Command and Random User
        # ------------------------------

        parser = ParseTime(
            user=self.user,
            command=self.command,
            args=self.args,
            allow_random_sfx=True,
            allow_random_user=True,
        ).parse()

        if self.command in ["steal"]:

            if parser.target_user == "random" and parser.target_sfx == "random":
                parser.target_user = self.random_not_you_user()
                parser.target_sfx = random.sample(
                    User(parser.target_user).commands(), 1
                )[0]

            return CommandStealer(
                thief=self.user, victim=parser.target_user, command=parser.target_sfx,
            ).steal()

        if self.command in COMMANDS["give"]["aliases"]:

            if parser.target_command == "random":
                sfx_choices = random.choice(User(self.user).commands(), 1) - [self.user]
                parser.target_sfx = sfx_choices[0]
                print(f"Choosing Random Command: {parser.target_command}")

            if parser.target_user == "random":
                command = Command(parser.target_sfx)
                parser.target_user = find_random_user(
                    blacklisted_users=[command.users()] + [self.user]
                )

            if parser.target_user is None:
                raise ValueError("We didn't find a user to give to")

            print(f"Attempting to give: !{parser.target_sfx} @{parser.target_user}")

            # This interface needs to call Command SFX
            return CommandGiver(
                user=self.user, command=parser.target_sfx, friend=parser.target_user,
            ).give()

        # -------------------
        # Stream God Commands
        # -------------------

        if self.command == "dropeffect" and self.user in STREAM_GODS:
            parser = PropsParser(user=self.user, args=self.args).parse()
            parser2 = PermsParser(user=self.user, args=self.args).parse()

            return Airdrop(
                target_user=parser.target_user,
                target_command=parser2.target_command,
                amount=parser.amount,
            ).drop()

        if self.command == "dropreward" and self.user in STREAM_GODS:
            return dropreward()

        # ------------------
        # OBS or Soundeffect
        # ------------------

        if self.command in OBS_COMMANDS and self.user in STREAM_LORDS:
            print(f"executing OBS Command: {self.command}")
            return os.system(f"so {self.command}")

        if self.command:
            PlaySoundeffectRequest(user=self.user, command=self.command).save()

    def random_not_you_user(self):
        return find_random_user(blacklisted_users=[self.user])
