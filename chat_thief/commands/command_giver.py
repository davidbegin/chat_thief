import random

from chat_thief.permissions_manager import PermissionsManager
from chat_thief.models.user import User

class CommandGiver:
    def __init__(self, user, command, friend):
        self.user = user
        self.command = command
        self.friend = friend

    def give(self):
        return PermissionsManager(
            user=self.user, command=self.command, args=[self.command, self.friend],
        ).swap_perm()
