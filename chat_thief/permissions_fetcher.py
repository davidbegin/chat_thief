from chat_thief.models.user import User
from chat_thief.models.command import Command


class PermissionsFetcher:
    @classmethod
    def fetch_permissions(cls, user, target_command, target_user):
        # Personal Permissions
        if not target_command and not target_user:
            user = User(user)
            stats = user.stats()
            user_permissions = " ".join([f"!{perm}" for perm in user.commands()])
            return f"{stats} | {user_permissions}"

        # User Permissions
        if target_user and not target_command:
            title = f"@{target_user}'s"
            user_permissions = " ".join(
                [f"!{perm}" for perm in User(target_user).commands()]
            )
            return f"{title} Permissions: {user_permissions}"

        # Command Permissions
        if target_command and not target_user:
            command = Command(target_command)
            user_permissions = " ".join([f"@{perm}" for perm in command.users()])

            from chat_thief.models.sfx_vote import SFXVote

            like_ratio = SFXVote(target_command).like_to_hate_ratio()
            stats = f"!{target_command} | Cost: {command.cost()} | Health: {command.health()} | Like Ratio {round(like_ratio)}%"
            if user_permissions:
                stats += f" | {user_permissions}"
            return stats
