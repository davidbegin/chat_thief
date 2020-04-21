from chat_thief.permissions_manager import PermissionsManager
from chat_thief.user import User

class CommandSharer:
    def __init__(self, user, command, friend):
        self.user = user
        self.command = command
        self.friend = friend

    def share(self):
        if User(self.user).street_cred() > 0:
            print(f"\n{self.user} has enough street_cred!")

            # We are using permissions manager wrong
            perm_result = PermissionsManager(
                user=self.user, command=self.command, args=[self.command, self.friend],
            ).add_perm()

            if perm_result:
                print("\nWe have a Perm Result")
                User(self.user).remove_street_cred()
                return perm_result
            else:
                print("\nWe NOOOOO have a Perm Result")
                return f"{self.user} cannot add permissions"
        else:
            return "@{self.user} Not enough street_cred to share !{self.command} with @{self.friend}"
