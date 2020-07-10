from typing import Optional, Dict, List

from chat_thief.models.user import User
from chat_thief.models.command import Command

from chat_thief.prize_dropper import random_user


class Donator:
    def __init__(self, user: str):
        self.user = user

    def donate(self, target_user: Optional[str] = None) -> str:
        results: Dict[str, List[str]] = {}

        for command_name in User(self.user).commands():
            if command_name == self.user:
                continue

            command = Command(command_name)  # This is a Command

            # so we we have a user use it
            # if not donate to randos
            if target_user:
                new_user = target_user
            else:
                new_user = random_user(blacklisted_users=command.users())

            if new_user:
                donated_commands = results.get(new_user, [])
                results[new_user] = donated_commands + [command.name]
                command.allow_user(new_user)
                command.unallow_user(self.user)

        return " ".join(
            [
                f"@{user} was gifted {' '.join([f'!{command}' for command in commands])}"
                for user, commands in results.items()
            ]
        )
