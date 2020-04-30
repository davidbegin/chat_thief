from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.models.command import Command
from chat_thief.models.database import COMMANDS_DB_PATH


# PermissionsManager is the merger of User with Command!!!
class PermissionsManager:
    def __init__(
        self,
        user,
        command=None,
        target_command=None,
        target_user=None,
        commands_db_path=COMMANDS_DB_PATH,
        skip_validation=False,
    ):
        self.user = user
        self.command = command
        self.skip_validation = skip_validation
        self.target_command = target_command
        self.target_user = target_user
        self.command = Command(name=self.target_command)

    def swap_perm(self):
        permitted_users = self.command.users()

        if self.user in STREAM_GODS:
            return f"YOU'RE A STREAM GOD @{self.user} YOU DON'T NEED TO SWAP PERMS"
        else:
            print(f"Permitted Users For: !{self.target_command} {permitted_users}")
            if self.user in permitted_users:
                allow_msg = self.command.allow_user(self.target_user)
                return [allow_msg, self.command.unallow_user(self.user)]
            else:
                return f"@{self.user} does not have permission to give: {self.target_command}"

    def add_perm(self):
        permitted_users = self.command.users()

        if self.user in STREAM_GODS:
            return self.command.allow_user(self.target_user)
        else:
            print(f"!{self.target_command} Permitted Users: {permitted_users}")
            if self.user in permitted_users:
                return self.command.allow_user(self.target_user)
