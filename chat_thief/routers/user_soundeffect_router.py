from chat_thief.routers.base_router import BaseRouter
from chat_thief.models.user import User
from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.permissions_fetcher import PermissionsFetcher


class UserSoundeffectRouter(BaseRouter):
    def route(self):
        # -------------------------
        # No Random Command or User
        # -------------------------

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
