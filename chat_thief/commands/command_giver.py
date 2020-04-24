import random

from chat_thief.permissions_manager import PermissionsManager
from chat_thief.models.user import User

class CommandGiver:
    def __init__(self, user, command, friend):
        self.user = user
        self.command = command
        self.friend = friend

        if self.command == "random":
            command = random.sample(User(self.user).commands(), 1)[0]
            print(f"Fetching Random Command!: {command}")
            self.command = command

        if self.friend == "random":
            from chat_thief.prize_dropper import random_user
            self.friend = random_user()

    def give(self):
        # if self.command is None:
        # if self.friend is None:
        return PermissionsManager(
            user=self.user, command=self.command, args=[self.command, self.friend],
        ).swap_perm()
