from chat_thief.models.user import Command

from chat_thief.config.stream_lords import STREAM_GODS


class CommandGiver:
    def __init__(self, user, command, friend):
        self.user = user
        self.command = command
        self.friend = friend

    def give(self):
        if self.user in STREAM_GODS:
            return f"YOU'RE A STREAM GOD @{self.user} YOU DON'T NEED TO SWAP PERMS"

        permitted_users = Command(self.command).users()
        print(f"Permitted Users For: !{self.command} {permitted_users}")

        command = Command(self.command)
        if self.user in permitted_users:
            allow_msg = command.allow_user(self.friend)
            return [allow_msg, command.unallow_user(self.user)]

        return f"@{self.user} does not have permission to give: !{self.command}"
