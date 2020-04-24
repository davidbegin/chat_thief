from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.audio_command import AudioCommand
from chat_thief.models.database import USERS_DB_PATH, COMMANDS_DB_PATH


# We need to update this to not take args
class PermissionsManager:
    def __init__(
        self,
        user,
        command=None,
        target_command=None,
        target_user=None,
        users_db_path=USERS_DB_PATH,
        commands_db_path=COMMANDS_DB_PATH,
        skip_validation=False,
    ):
        self.user = user
        self.command = command
        self.skip_validation = skip_validation

        self.target_command = target_command
        self.target_user = target_user

        self.audio_command = AudioCommand(
            self.target_command,
            skip_validation=skip_validation,
            commands_db_path=commands_db_path,
        )

    def swap_perm(self):
        permitted_users = self.audio_command.permitted_users()

        if self.user in STREAM_GODS:
            return f"YOU'RE A STREAM GOD @{self.user} YOU DON'T NEED TO SWAP PERMS"
        else:
            print(f"Permitted Users For: {self.target_command} {permitted_users}")

            if self.user in permitted_users:
                allow_msg = self.audio_command.allow_user(self.target_user)
                # If you try and swap a command you don't own, you lose access
                return [allow_msg, self.audio_command.unallow_user(self.user)]
            else:
                return f"{self.user} does not have permission to give: {self.target_command}"

    def add_perm(self):
        permitted_users = self.audio_command.permitted_users()

        if self.user in STREAM_GODS:
            return self.audio_command.allow_user(self.target_user)
        else:
            print(f"!{self.target_command} Permitted Users: {permitted_users}")

            if self.user in permitted_users:
                return self.audio_command.allow_user(self.target_user)
