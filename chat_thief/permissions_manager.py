from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.models.command import Command


# PermissionsManager is the merger of User with Command!!!
class PermissionsManager:
    def __init__(
        self,
        user,
        command=None,
        target_command=None,
        target_user=None,
    ):
        self.user = user
        self.target_command = target_command
        self.target_user = target_user
        self.command = Command(name=self.target_command)

    def add_perm(self):
        permitted_users = self.command.users()

        if self.user in STREAM_GODS:
            return self.command.allow_user(self.target_user)
        else:
            print(f"!{self.target_command} Permitted Users: {permitted_users}")
            if self.user in permitted_users:
                return self.command.allow_user(self.target_user)
