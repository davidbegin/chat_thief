from chat_thief.routers.base_router import BaseRouter
from chat_thief.models.user import User
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.permissions_fetcher import PermissionsFetcher
from chat_thief.commands.donator import Donator
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
