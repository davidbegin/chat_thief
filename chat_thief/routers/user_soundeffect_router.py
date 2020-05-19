import random

from chat_thief.prize_dropper import random_user as find_random_user
from chat_thief.models.user import User
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.commands.command_stealer import CommandStealer
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.commands.donator import Donator
from chat_thief.commands.street_cred_transfer import StreetCredTransfer
from chat_thief.routers.base_router import BaseRouter
from chat_thief.models.sfx_vote import SFXVote


class UserSoundeffectRouter(BaseRouter):
    def route(self):
        parser = CommandParser(
            user=self.user, command=self.command, args=self.args
        ).parse()

        if self.command in ["me"]:
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

        if self.command in ["support", "love", "like"]:
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

            return CommandStealer(
                thief=self.user, victim=parser.target_user, command=parser.target_sfx,
            ).steal()

    # What a Terrible Name
    def _random_user(self):
        return find_random_user(blacklisted_users=[self.user])
