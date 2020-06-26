from chat_thief.models.user import User
from chat_thief.models.command import Command

# TODO: unduplicate
BASE_URL = "https://mygeoangelfirespace.city"


class PermissionsFetcher:
    @classmethod
    def fetch_permissions(cls, user, target_command, target_user):
        # Personal Permissions
        if not target_command and not target_user:
            user = User(user)
            stats = user.stats()
            sfx_count = len(user.commands())
            return f"{stats} | SFX Count: {sfx_count}"

        # User Permissions
        if target_user and not target_command:
            title = f"@{target_user}'s"
            sfx_count = len(User(target_user).commands())
            stats = User(target_user).stats()
            return f"{title} {stats} | SFX Count: {sfx_count}"

        # Command Permissions
        if target_command and not target_user:
            command = Command(target_command)
            user_permissions = " ".join([f"@{perm}" for perm in command.users()])

            from chat_thief.models.sfx_vote import SFXVote

            link = f"{BASE_URL}/commands/{target_command}.html"
            like_ratio = SFXVote(target_command).like_to_hate_ratio()
            stats = f"!{target_command} | Cost: {command.cost()} | Health: {command.health()} | Like Ratio {round(like_ratio)}% | {link}"
            return stats
