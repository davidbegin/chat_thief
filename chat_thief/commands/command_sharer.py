from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.config.stream_lords import STREAM_GODS

from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary


class CommandSharer:
    def __init__(self, user: str, command: str, friend: str):
        self.user = user
        self.command = command
        self.friend = friend

    def share(self) -> str:
        if not self.command in SoundeffectsLibrary.fetch_soundeffect_names():
            return f"@{self.user} cannot share !{self.command} as it's invalid"

        command = Command(name=self.command)
        command_cost = command.cost()
        user_cool_points = User(self.user).cool_points()

        if self.user in STREAM_GODS:
            perm_result = command.allow_user(self.friend)
            return f"{self.user} shared {perm_result}"

        elif user_cool_points >= command_cost:
            perm_result = command.allow_user(self.friend)
            if perm_result:
                print("\nWe have a Perm Result")
                User(self.user).update_cool_points(-command_cost)
                command.increase_cost(command_cost * 2)
                return f"{self.user} shared {perm_result}"
            else:
                print("\nWe NOOOOO have a Perm Result")
                return f"{self.user} cannot add permissions"

        else:
            return f"@{self.user} Not enough cool_points ({user_cool_points}/{command_cost}) to share !{self.command} with @{self.friend}"
