from chat_thief.stream_lords import STREAM_LORDS, STREAM_GODS
from chat_thief.audio_command import AudioCommand
from chat_thief.database import USERS_DB_PATH, COMMANDS_DB_PATH


class PermissionsManager:
    def __init__(
        self,
        user,
        command=None,
        args=[],
        users_db_path=USERS_DB_PATH,
        commands_db_path=COMMANDS_DB_PATH,
        skip_validation=False,
    ):
        if len(args) < 2:
            print("you need more args: command user!")
            raise ArgumentError

        self.user = user
        self.command = command
        self.skip_validation = skip_validation

        self.target_command = args[0].lower()
        self.target_user = args[1].lower()
        self.audio_command = AudioCommand(
            self.target_command,
            skip_validation=skip_validation,
            commands_db_path=commands_db_path,
        )

    def add_perm(self):
        permitted_users = self.audio_command.permitted_users()

        if self.user in STREAM_GODS:
            return self.audio_command.allow_user(self.target_user)
        else:
            print(f"Permitted Users For: {self.target_command} {permitted_users}")

            if self.user in permitted_users:
                return self.audio_command.allow_user(self.target_user)
            else:
                print(f"{self.user} cannot add permissions")
