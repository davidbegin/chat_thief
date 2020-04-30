from chat_thief.models.user import User
from chat_thief.models.command import Command


class PermissionsFetcher:

    @classmethod
    def fetch_permissions(cls, user, target_command, target_user):
        # Personal Permissions
        if not target_command and not target_user:
            title = f"@{user}'s"
            user_permissions = " ".join([f"!{perm}" for perm in User(user).commands() ])
            return f"{title} Permissions: {user_permissions}"

        # User Permissions
        if target_user and not target_command:
            title = f"@{target_user}'s"
            user_permissions = " ".join([f"!{perm}" for perm in User(target_user).commands() ])
            return f"{title} Permissions: {user_permissions}"

        # Command Permissions
        if target_command and not target_user:
            title = f"!{target_command}'s"
            user_permissions = " ".join([f"@{perm}" for perm in Command(target_command).users() ])
            return f"{title} Permissions: {user_permissions}"
