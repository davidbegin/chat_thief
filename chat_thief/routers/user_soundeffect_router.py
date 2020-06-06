from pathlib import Path
import random

import requests

from chat_thief.prize_dropper import random_user as find_random_user
from chat_thief.models.user import User
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.commands.command_stealer import CommandStealer
from chat_thief.commands.command_giver import CommandGiver
from chat_thief.commands.command_sharer import CommandSharer
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.commands.donator import Donator
from chat_thief.commands.street_cred_transfer import StreetCredTransfer
from chat_thief.routers.base_router import BaseRouter
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.command import Command
from chat_thief.commands.command_buyer import CommandBuyer
from chat_thief.config.stream_lords import STREAM_LORDS

BASE_URL = "https://www.beginworld.exchange"

COMMANDS = {"give": {"aliases": ["transfer", "give"],}}


class UserSoundeffectRouter(BaseRouter):
    def route(self):
        # This is the default parser
        # if a command wants to handle more
        # custom parser, they just use their own parser
        parser = CommandParser(
            user=self.user, command=self.command, args=self.args
        ).parse()

        if self.command == "css":
            if self.user in STREAM_LORDS:
                return self.set_css()

        if self.command in ["me", "perm"]:
            return self.me()

        if self.command in ["permissions", "permission", "perms", "perm"]:
            return self.perms(parser)

        if self.command == "donate":
            return self.donate(parser)

        if self.command in ["love", "like"]:
            return self.love(parser)

        if self.command in ["dislike", "hate", "detract"]:
            return self.hate(parser)

        if self.command in [
            "props",
            "bigups",
            "endorse",
        ]:
            return self.props()

        if self.command in ["steal"]:
            return self.steal()

        if self.command in ["buy"]:
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

    def donate(self, parser):
        if parser.target_user:
            return Donator(self.user).donate(parser.target_user)
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
        # stats = User(self.user).stats()
        return f"{BASE_URL}/{self.user}.html"

    def perms(self, parser):
        if len(self.args) > 0 and not parser.target_sfx and not parser.target_user:
            raise ValueError(f"Could not find user or command: {' '.join(self.args)}")
        return PermissionsFetcher.fetch_permissions(
            user=self.user,
            target_user=parser.target_user,
            target_command=parser.target_sfx,
        )

    def buy(self):
        parser = CommandParser(
            user=self.user, command=self.command, args=self.args, allow_random_sfx=True,
        ).parse()

        return CommandBuyer(
            user=self.user, target_sfx=parser.target_sfx, amount=parser.amount
        ).new_buy()

    def share(self):
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
                parser.target_user = find_random_user(
                    blacklisted_users=Command(parser.target_sfx).users()
                )

        if parser.target_user and parser.target_sfx:
            return CommandSharer(
                self.user, parser.target_sfx, parser.target_user
            ).share()
        else:
            return f"Error Sharing - Command: {parser.target_sfx} | User: {parser.target_user}"

    def steal(self):
        parser = CommandParser(
            user=self.user,
            command=self.command,
            args=self.args,
            allow_random_sfx=True,
            allow_random_user=True,
        ).parse()

        # here is where we are habing a problem
        if parser.target_user == "random" and parser.target_sfx == "random":
            looking_for_user = True
            attempts = 0
            while looking_for_user:
                parser.target_user = self._random_user()
                attempts += 1
                commands = User(parser.target_user).commands()

                if len(commands) > 0:
                    looking_for_user = False
                    parser.target_sfx = random.sample(commands, 1)[0]
                elif attempts > 5:
                    raise RuntimeError("Can't find user with commands to steal")

        if parser.target_user and parser.target_sfx:
            return CommandStealer(
                thief=self.user, victim=parser.target_user, command=parser.target_sfx,
            ).steal()
        else:
            return f"@{self.user} failed to steal: {' '.join(self.args)}"

    def give(self):
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

    def props(self):
        parser = CommandParser(
            user=self.user,
            command=self.command,
            args=self.args,
            allow_random_user=True,
        ).parse()
        # Here is the bug,
        # this needs to occur inside the streetcred transfer
        # if parser.target_user == "random" or parser.target_user is None:
        #     parser.target_user = self._random_user()

        return StreetCredTransfer(
            user=self.user, cool_person=parser.target_user, amount=parser.amount
        ).transfer()

    def love(self, parser):
        if parser.target_sfx and not parser.target_user:
            result = SFXVote(parser.target_sfx).support(self.user)
            love_count = len(result["supporters"])
            hate_count = len(result["detractors"])
            return f"!{parser.target_sfx} supporters: {love_count} | detractors {hate_count}"

        if parser.target_user and not parser.target_sfx:
            if self.user == parser.target_user:
                return f"You can love yourself in real life, but not in Beginworld @{self.user}"
            else:
                User(self.user).set_ride_or_die(parser.target_user)
                return f"@{self.user} Made @{parser.target_user} their Ride or Die"
        else:
            return None

    def hate(self, parser):
        if parser.target_sfx and not parser.target_user:
            result = SFXVote(parser.target_sfx).detract(self.user)
            love_count = len(result["supporters"])
            hate_count = len(result["detractors"])
            return f"!{parser.target_sfx} supporters: {love_count} | detractors {hate_count}"
        else:
            return f"We are not sure who or what you trying to hate. Maybe try and focusing your hate better next time @{self.user}"
