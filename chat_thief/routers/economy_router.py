from typing import Optional, List, Dict, Union, Any
from pathlib import Path
import random

import requests

from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.commands.command_giver import CommandGiver
from chat_thief.commands.command_sharer import CommandSharer
from chat_thief.commands.donator import Donator
from chat_thief.commands.street_cred_transfer import StreetCredTransfer
from chat_thief.config.stream_lords import STREAM_LORDS
from chat_thief.current_stream import CurrentStream
from chat_thief.formatters.steal_formatter import StealFormatter
from chat_thief.models.command import Command
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.user import User
from chat_thief.new_commands.buyer import Buyer, PurchaseResult
from chat_thief.new_commands.stealer import Stealer
from chat_thief.new_commands.result import Result
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.prize_dropper import random_user as find_random_user
from chat_thief.routers.base_router import BaseRouter
from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.prize_dropper import drop_effect

BASE_URL = "https://mygeoangelfirespace.city"

COMMANDS = {"give": {"aliases": ["transfer", "give"],}}


class EconomyRouter(BaseRouter):
    def route(self) -> Optional[Union[List[str], str]]:
        if self.command in  ["insurance", "insure"]:
            return User(self.user).buy_insurance()

        if self.command == "archpack" and self.user in STREAM_GODS:
            return [
                drop_effect(self.parser.target_user,"arch"),
                drop_effect(self.parser.target_user,"archluke"),
                drop_effect(self.parser.target_user,"gcc")
            ]

        if self.command == "commands":
            cmd_list = " | ".join(User(self.user).commands())
            return f"@{self.user} Commands: {cmd_list}"

        if self.command == "css":
            # if self.user in STREAM_LORDS:
            return self.set_css()

        if self.command in ["me", "perm"]:
            return self.me()

        if self.command in ["permissions", "permission", "perms", "perm"]:
            return self.perms()

        if self.command == "donate":
            return self.donate()

        if self.command in ["love", "like"]:
            return self.love()

        if self.command in ["dislike", "hate", "detract"]:
            return self.hate()

        if self.command in [
            "props",
            "bigups",
            "endorse",
        ]:
            return self.props()

        if self.command in ["steal"]:
            return self.steal()

        if self.command == "buy":
            return self.buy()

        # So What are the aliases here
        if self.command in COMMANDS["give"]["aliases"]:
            return self.give()

        if self.command in [
            "share",
            "clone",
            "add_perm",
            "add_perms",
            "share_perm",
            "share_perms",
        ]:
            return self.share()

    def donate(self):
        if self.parser.target_user:
            return Donator(self.user).donate(self.parser.target_user)
        else:
            return Donator(self.user).donate()

    # What a Terrible Name
    def _random_user(self):
        return find_random_user(blacklisted_users=[self.user])

    def set_css(self):
        custom_css = self.args[0]
        User(self.user).set_value("custom_css", custom_css)

        # Switch to NOT USE requests
        response = requests.get(custom_css)
        new_css_path = Path(__file__).parent.parent.joinpath(f"static/{self.user}.css")
        print(f"Saving Custom CSS for @{self.user} {new_css_path}")
        with open(new_css_path, "w") as f:
            f.write(response.text)

        return f"Thanks for the custom CSS @{self.user}! {BASE_URL}/{self.user}.html"

    def me(self):
        stats = User(self.user).stats()
        return f"{stats} | {BASE_URL}/{self.user}.html"

    def perms(self) -> str:
        if (
            len(self.args) > 0
            and not self.parser.target_sfx
            and not self.parser.target_user
        ):
            raise ValueError(f"Could not find user or command: {' '.join(self.args)}")

        return PermissionsFetcher.fetch_permissions(
            user=self.user,
            target_user=self.parser.target_user,
            target_command=self.parser.target_sfx,
        )

    def buy(self) -> Union[List, str]:
        parser = CommandParser(
            user=self.user, command=self.command, args=self.args, allow_random_sfx=True,
        ).parse()

        result = Buyer(
            user=self.user, target_sfx=parser.target_sfx, amount=parser.amount
        ).buy()

        return self._format_result(result)

    def share(self) -> str:
        parser = CommandParser(
            user=self.user,
            command=self.command,
            args=self.args,
            allow_random_sfx=True,
            allow_random_user=True,
        ).parse()

        if parser.target_sfx == "random":
            commands = User(self.user).commands()
            parser.target_sfx = random.sample(commands, 1)[0]

        if parser.target_user == "random" or parser.target_user is None:
            if parser.target_sfx:
                blacklisted_users = Command(parser.target_sfx).users()
                random_user = CurrentStream.random_user(blacklisted_users)
                parser.target_user = random_user

        if parser.target_user and parser.target_sfx:
            return CommandSharer(
                self.user, parser.target_sfx, parser.target_user
            ).share()
        else:
            return f"Error Sharing - Command: {parser.target_sfx} | User: {parser.target_user}"

    def steal(self) -> str:
        if self.parser.target_user and self.parser.target_sfx:
            result = Stealer(
                thief=self.user,
                victim=self.parser.target_user,
                target_sfx=self.parser.target_sfx,
            ).steal()

            if User(self.parser.target_user).creator() == self.user:
                return f"You cannot steal from your own bot @{self.user} @{self.parser.target_user}"
            elif User(self.user).creator() == self.parser.target_user:
                return f"You cannot steal from your creator @{self.user} @{self.parser.target_user}"
            else:
                return StealFormatter(result).format()
        else:
            msg = f"@{self.user} you must specify who and what you want to steal."
            if self.args:
                msg += f" Invalid Args: {' '.join(self.args)}"
            return msg

    def give(self) -> str:
        parser = CommandParser(
            user=self.user,
            command=self.command,
            args=self.args,
            allow_random_sfx=True,
            allow_random_user=True,
        ).parse()

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

    def props(self) -> str:
        parser = CommandParser(
            user=self.user,
            command=self.command,
            args=self.args,
            allow_random_user=True,
        ).parse()

        target_user_creator = User(parser.target_user).creator()
        user_creator = User(self.user).creator()

        target_user = parser.target_user
        top_eight = []

        if parser.target_user == "random" or parser.target_user is None:
            top_eight = [
                friend
                for friend in User(self.user).top_eight()
                if User(friend).creator() != self.user
            ]
            if top_eight == []:
                return f"@{self.user} You must specify a Top8 to give random props (Bots Don't count). !top8 @user"

        if target_user_creator == self.user:
            return f"You cannot props your own bot @{self.user} @{parser.target_user}"

        elif user_creator and user_creator == parser.target_user:
            return f"You cannot props your creator @{self.user} @{parser.target_user}"

        # target_user = random.sample( top_eight, 1)[0]
        return StreetCredTransfer(
            user=self.user,
            cool_person=target_user,
            top_eight=top_eight,
            amount=parser.amount,
        ).transfer()

    def love(self) -> Optional[str]:
        if self.parser.target_sfx and not self.parser.target_user:
            result = SFXVote(self.parser.target_sfx).support(self.user)
            love_count = len(result["supporters"])
            hate_count = len(result["detractors"])
            return f"!{self.parser.target_sfx} supporters: {love_count} | detractors {hate_count}"

        if self.parser.target_user and not self.parser.target_sfx:
            if self.user == self.parser.target_user:
                return f"You can love yourself in real life, but not in Beginworld @{self.user}"
            else:
                User(self.user).set_ride_or_die(self.parser.target_user)
                return f"@{self.user} Made @{self.parser.target_user} their Ride or Die"
        else:
            return None

    def hate(self) -> str:
        if self.parser.target_sfx and not self.parser.target_user:
            result = SFXVote(self.parser.target_sfx).detract(self.user)
            love_count = len(result["supporters"])
            hate_count = len(result["detractors"])
            return f"!{self.parser.target_sfx} supporters: {love_count} | detractors {hate_count}"
        else:
            return f"We are not sure who or what you trying to hate. Maybe try and focusing your hate better next time @{self.user}"

    def _format_result(self, result: Result) -> Union[List, str]:
        if "purchase_results" in result.metadata:
            results = result.metadata["purchase_results"]

            total_spent = sum([result.cost for result in results])
            sfx_names = " ".join(["!" + result.sfx for result in results])

            successful_purchase = all(
                [
                    result.result == PurchaseResult.SuccessfulPurchase
                    for result in results
                ]
            )
            if successful_purchase:
                return f"@{self.user} bought {len(results)} SFXs: {sfx_names} for a Total of {total_spent} Cool Points"
            else:
                if len(results) == 1:
                    return results[0].message
                else:
                    return [result.message for result in results]
