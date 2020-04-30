from chat_thief.models.user import User
from chat_thief.config.stream_lords import STREAM_GODS


class CommandSharer:
    def __init__(self, user, command, friend):
        self.user = user
        self.command = command
        self.friend = friend

    def share(self):
        if self.user in STREAM_GODS:
            command = Command(name=self.command)
            return self.command.allow_user(self.friend)
        elif User(self.user).street_cred() > 0:
            command = Command(name=self.command)
            perm_result = self.command.allow_user(self.friend)

            if perm_result:
                print("\nWe have a Perm Result")
                User(self.user).remove_street_cred()
                return perm_result
            else:
                print("\nWe NOOOOO have a Perm Result")
                return f"{self.user} cannot add permissions"
        else:
            return f"@{self.user} Not enough street_cred to share !{self.command} with @{self.friend}"
