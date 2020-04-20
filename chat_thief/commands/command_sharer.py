from chat_thief.permissions_manager import PermissionsManager
from chat_thief.user import User

class CommandSharer:
    def __init__(self, user, command, friend):
        self.user = user
        self.command = command
        self.friend = friend

    def share(self):
        if User(self.user).street_cred() > 0:
            User(self.user).remove_street_cred()
            return PermissionsManager(
                user=self.user, command=self.command, args=[self.friend],
            ).add_perm()
        else:
            return "@{self.user} Not enough street_cred to share !{self.command} with @{self.friend}"
