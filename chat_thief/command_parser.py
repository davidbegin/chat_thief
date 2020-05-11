from typing import Dict, List, Optional
import logging
import os

from chat_thief.prize_dropper import random_user as find_random_user
from chat_thief.chat_parsers.request_approver_parser import RequestApproverParser
from chat_thief.chat_parsers.perms_parser import PermsParser
from chat_thief.chat_parsers.props_parser import PropsParser
from chat_thief.chat_parsers.soundeffect_request_parser import SoundeffectRequestParser

from chat_thief.economist.facts import Facts
from chat_thief.commands.command_sharer import CommandSharer
from chat_thief.commands.cube_casino import CubeCasino
from chat_thief.commands.leaderboard import leaderboard, loserboard
from chat_thief.commands.revolution import Revolution
from chat_thief.commands.shoutout import shoutout
from chat_thief.commands.street_cred_transfer import StreetCredTransfer
from chat_thief.commands.command_stealer import CommandStealer
from chat_thief.commands.command_giver import CommandGiver
from chat_thief.commands.donator import Donator
from chat_thief.commands.la_libre import LaLibre

from chat_thief.models.command import Command
from chat_thief.models.cube_bet import CubeBet
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


BLACKLISTED_LOG_USERS = [
    # "beginbotbot",
    # "beginbot",
    "nightbot",
]

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
    "most_popular": "!most_popular - Shows the most coveted commands",
    "soundeffect": "!soundeffect YOUTUBE-ID YOUR_USERNAME 00:01 00:05 - Must be less than 5 second",
}

COMMANDS = {
    "give": {
        "aliases": ["transfer"],
        "help": "!transfer COMMAND USER - transfer command to someone, costs no cool points",
    }
}

WARNING = "\033[93m"
WARNING = "\033[92m"
FAIL = "\033[91m"
OK = "\033[92m"


CLEAR = "\033[0m"


class CommandParser:
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

        return self._process_command()

    def _process_command(self):
        if self.command in ["peace", "revolution", "vote"]:
            if self.command == "vote":
                vote = self.args[0]
                Vote(user=self.user).vote(vote)
            else:
                Vote(user=self.user).vote(self.command)

            return f"Thank you for your vote @{self.user}"

        if self.command == "facts" and self.user in STREAM_GODS:
            return Facts().available_sounds()

        if self.command == "coup_cost" and self.user in STREAM_GODS:
            return Command("coup").increase_cost(-3)

        if self.command == "richest":
            return " | ".join(
                [f"{stat[0]}: {stat[1]}" for stat in reversed(User.richest())]
            )

        if self.command == "la_libre":
            return LaLibre.inform()

        # if self.command in ["leaderboard", "forbes"]:
        #     return leaderboard()

        # if self.command == "loserboard":
        #     return loserboard()

        if self.command == "requests":
            stats = SoundeffectRequest.formatted_stats()
            if not stats:
                stats = "Excellent Job Stream Lords No Requests!"
            return stats

        if self.command == "most_popular":
            return " | ".join(Command.most_popular())

        if self.command in ["economy"]:
            cool_points = User(self.user).total_cool_points()
            return f"Total Cool Points in Market: {cool_points}"

        if self.command == "users":
            return WelcomeCommittee().present_users()

        if self.command in ["all_bets", "all_bet", "bets"]:
            return " | ".join([f"@{bet[0]}: {bet[1]}" for bet in CubeBet.all_bets()])

        if self.command == "bet":
            parser = PropsParser(user=self.user, args=self.args).parse()
            result = CubeBet(name=self.user, duration=parser.amount).save()
            return f"Thank you for your bet: @{result['name']}: {result['duration']}s"

        if self.command == "new_cube" and self.user == "beginbotbot":
            return CubeCasino(self.user, self.args).purge()

        if self.command == "cubed" and self.user in ["beginbot", "beginbotbot"]:
            cube_time = int(self.args[0])
            result = CubeCasino(cube_time).gamble()
            CubeBet.purge()
            return result

        if self.command == "so":
            return shoutout(self.msg)

        if self.command == "streamlords":
            return " ".join(STREAM_LORDS)

        if self.command == "streamgods":
            return " ".join(STREAM_GODS)

        if self.command == "coup":
            viva_la_revolution = Revolution(self.user)

            from chat_thief.commands.la_libre import REVOLUTION_LIKELYHOOD

            threshold = int(User.count() / REVOLUTION_LIKELYHOOD)
            result = Vote.have_tables_turned(threshold)
            print(f"The Result of have_tables_turned: {result}")

            if result in ["peace", "revolution"]:
                return Revolution(self.user).attempt_coup(result)
            else:
                return f"The Will of the People have not chosen: {threshold} votes must be cast for either Peace or Revolution"

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

        if self.command == "bankrupt":
            parser = PermsParser(user=self.user, args=self.args).parse()
            if self.user in STREAM_GODS:
                return User(parser.target_user).bankrupt()

        if self.command == "paperup":
            parser = PermsParser(user=self.user, args=self.args).parse()
            if self.user in STREAM_GODS:
                return User(parser.target_user).paperup()

        if self.command in ["deny"] and self.user in STREAM_LORDS:
            parser = RequestApproverParser(user=self.user, args=self.args).parse()
            if parser.doc_id:
                SoundeffectRequest.deny_doc_id(self.user, parser.doc_id)
                return f"@{self.user} DENIED Request: {parser.doc_id}"

        if self.command in ["approve"] and self.user in STREAM_LORDS:
            # # This should take a parser and act accordingly
            # "!approve all"
            # "!approve 1"
            # "!approve @artmattdank"
            # "!approve !new_command"

            parser = RequestApproverParser(user=self.user, args=self.args).parse()

            if parser.target_user:
                return SoundeffectRequest.approve_user(self.user, parser.target_user)
            elif parser.target_command:
                return SoundeffectRequest.approve_command(
                    self.user, parser.target_command
                )
            elif parser.doc_id:
                return SoundeffectRequest.approve_doc_id(self.user, parser.doc_id)
            else:
                return "Not Sure What to Approve"

            # elif parser.approve_all:
            #     return SoundeffectRequest.approve_all(approver=self.user)

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
                User(self.user).set_ride_or_die(parser.target_user)
                return f"@{self.user} Made @{parser.target_user} their Ride or Die"
            else:
                return None

        # -----
        # Other
        # -----

        if self.command == "soundeffect":
            sfx_request = SoundeffectRequestParser(self.user, self.irc_msg.args)

            return SoundeffectRequest(
                user=self.user,
                youtube_id=sfx_request.youtube_id,
                command=sfx_request.command,
                start_time=sfx_request.start_time,
                end_time=sfx_request.end_time,
            ).save()

        # -------------------------
        # Takes a User OR a Command
        # -------------------------

        if self.command == "do_over" and self.user == "beginbotbot":
            print("WE ARE GOING FOR IT!")
            for user in User.all():
                User(user).bankrupt()
            for command_name in Command.db().all():
                command_name = command_name["name"]
                print(command_name)
                command = Command(command_name)
                for user in command.users():
                    print(command.unallow_user(user))
            return "Society now must rebuild"

        if self.command == "revive" and self.user in STREAM_GODS:

            parser = PermsParser(user=self.user, args=self.args).parse()

            if parser.target_command:
                print(f"We are attempting to revive: !{parser.target_command}")
                Command.find_or_create(parser.target_command)
                return Command(parser.target_command).revive()
            elif parser.target_user:
                return User(parser.target_user).revive()
            else:
                print(f"Not Sure who or what to silence: {self.args}")

        if self.command == "silence" and self.user in STREAM_GODS:
            parser = PermsParser(user=self.user, args=self.args).parse()

            if parser.target_command:
                print("We are attempting to silence")
                return Command(parser.target_command).silence()
            elif parser.target_user:
                return User(parser.target_user).kill()
            else:
                print(f"Not Sure who or what to silence: {self.args}")

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
                parser.target_user = find_random_user(blacklisted_users=[self.user])

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
            parser = PermsParser(
                user=self.user, args=self.args, random_command=True, perm_type="buy"
            ).parse()

            if parser.target_command:
                command = parser.target_command
            else:
                command = "random"

            if len(self.args) > 1:
                results = []
                for _ in range(0, int(self.args[1])):
                    command = "random"
                    results.append(User(self.user).buy(command))
                return f"@{self.user}" + " ".join(
                    [
                        "!" + command[len("@{self.user} purchased:") :]
                        for command in results
                    ]
                )
            else:
                return User(self.user).buy(command)

        # ------------------------------
        # Random Command and Random User
        # ------------------------------

        parser = PermsParser(
            user=self.user, args=self.args, random_command=True, random_user=True,
        ).parse()

        if self.command in ["steal"]:
            if parser.target_user == "random" and parser.target_command == "random":
                parser.target_user = find_random_user(blacklisted_users=[self.user])
                command = random.sample(User(parser.target_user).commands(), 1)[0]

            return CommandStealer(
                thief=self.user,
                victim=parser.target_user,
                command=parser.target_command,
            ).steal()

        if self.command in COMMANDS["give"]["aliases"]:
            if parser.target_command == "random":
                parser.target_command = random.choice(User(self.user).commands(), 1)[0]
                print(f"Choosing Random Command: {parser.target_command}")

            if parser.target_command == "random":
                command = Command(parser.target_command)
                parser.target_user = find_random_user(
                    blacklisted_users=[command.users()]
                )

            if parser.target_user is None:
                raise ValueError("We didn't find a user to give to")

            print(f"Attempting to give: !{parser.target_command} @{parser.target_user}")

            return CommandGiver(
                user=self.user,
                command=parser.target_command,
                friend=parser.target_user,
            ).give()

        # -------------------
        # Stream God Commands
        # -------------------

        # These Need Chat Parsers
        if self.command == "dropeffect" and self.user in STREAM_GODS:
            return drop_soundeffect(self.user, self.args)

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
