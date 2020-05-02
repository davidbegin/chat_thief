from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.prize_dropper import random_user


class Donator:
    def __init__(self, user):
        self.user = user

    def donate(self):
        results = {}
        for command in User(self.user).commands():
            command = Command(command)
            new_user = random_user(blacklisted_users=command.users())
            if new_user:
                donated_commands = results.get(new_user, [])
                results[new_user] = donated_commands + [command.name]
                command.allow_user(new_user)
                command.unallow_user(self.user)
        return [
            f"@{user} was gifted {' '.join([f'!{command}' for command in commands])}"
            for user, commands in results.items()
        ]
