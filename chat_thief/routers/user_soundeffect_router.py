import random

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

BASE_URL = "http://beginworld.exchange-f27cf15.s3-website-us-west-2.amazonaws.com"

COMMANDS = {
    "give": {
        "aliases": ["transfer", "give"],
        # "help": "!transfer COMMAND USER - transfer command to someone, costs no cool points",
    }
}


class UserSoundeffectRouter(BaseRouter):
    def route(self):
        parser = CommandParser(
            user=self.user, command=self.command, args=self.args
        ).parse()

        if self.command in ["me", "perm"]:
            # return f"{BASE_URL}/{self.user}.html"

            user_permissions = " ".join(
                [f"!{perm}" for perm in User(self.user).commands()]
            )
            stats = User(self.user).stats()
            if user_permissions:
                return f"{stats} | {user_permissions}"
            else:
                return stats

        # TODO: This only works for soundeffects
        if self.command in ["permissions", "permission", "perms", "perm"]:
            if len(self.args) > 0 and not parser.target_sfx and not parser.target_user:
                raise ValueError(
                    f"Could not find user or command: {' '.join(self.args)}"
                )
            return PermissionsFetcher.fetch_permissions(
                user=self.user,
                target_user=parser.target_user,
                target_command=parser.target_sfx,
            )

        # ------------
        # Takes a User
        # ------------

        if self.command == "donate":
            if parser.target_user:
                return Donator(self.user).donate(parser.target_user)
            else:
                return Donator(self.user).donate()

        if self.command in ["love", "like"]:
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

        if self.command in ["dislike", "hate", "detract"]:
            if parser.target_sfx and not parser.target_user:
                result = SFXVote(parser.target_sfx).detract(self.user)
                love_count = len(result["supporters"])
                hate_count = len(result["detractors"])
                return f"!{parser.target_sfx} supporters: {love_count} | detractors {hate_count}"
            else:
                print("Doing Nothing")
                return

        if self.command in [
            "props",
            "bigups",
            "endorse",
        ]:
            parser = CommandParser(
                user=self.user, command=self.command, args=self.args
            ).parse()

            if parser.target_user == "random" or parser.target_user is None:
                parser.target_user = self._random_user()

            return StreetCredTransfer(
                user=self.user, cool_person=parser.target_user, amount=parser.amount
            ).transfer()

        parser = CommandParser(
            user=self.user,
            command=self.command,
            args=self.args,
            allow_random_sfx=True,
            allow_random_user=True,
        ).parse()

        if self.command in ["steal"]:
            if parser.target_user == "random" and parser.target_sfx == "random":
                parser.target_user = self._random_user()
                parser.target_sfx = random.sample(
                    User(parser.target_user).commands(), 1
                )[0]

            if parser.target_user and parser.target_sfx:
                return CommandStealer(
                    thief=self.user,
                    victim=parser.target_user,
                    command=parser.target_sfx,
                ).steal()
            else:
                return f"@{self.user} failed to steal: {' '.join(self.args)}"
                # return f"Problem stealing {parser.target_command} {self.args}"

        if self.command in ["buy"]:
            parser = CommandParser(
                user=self.user,
                command=self.command,
                args=self.args,
                allow_random_sfx=True,
            ).parse()

            return CommandBuyer(
                user=self.user, target_sfx=parser.target_sfx, amount=parser.amount
            ).new_buy()

        # So What are the aliases here
        if self.command in COMMANDS["give"]["aliases"]:
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

        if self.command in [
            "share",
            "clone",
            "add_perm",
            "add_perms",
            "share_perm",
            "share_perms",
        ]:
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

            # We  don't know why
            if parser.target_user and parser.target_sfx:
                return CommandSharer(
                    self.user, parser.target_sfx, parser.target_user
                ).share()
            else:
                return f"Error Sharing - Command: {parser.target_sfx} | User: {parser.target_user}"

    # What a Terrible Name
    def _random_user(self):
        return find_random_user(blacklisted_users=[self.user])
