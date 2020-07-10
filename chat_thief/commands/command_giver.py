from typing import List, Union

from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.custom_types import ChatReturnMessage


class CommandGiver:
    def __init__(self, user: str, command: str, friend: str):
        self.user = user
        self.command = command
        self.friend = friend

        if user == friend:
            raise ValueError("You cannot transfer sounds to yourself")

    def give(self) -> ChatReturnMessage:
        if self.user in STREAM_GODS:
            return f"YOU'RE A STREAM GOD @{self.user} YOU DON'T NEED TO SWAP PERMS"

        command = Command(self.command)
        permitted_users = command.users()

        if self.user in permitted_users:
            if self.friend in permitted_users:
                return (
                    f"@{self.friend} already has access to !{self.command} @{self.user}"
                )
            else:
                allow_msg = command.allow_user(self.friend)
                # TODO: revist and potentially don't return the unallowe
                # statement
                return [allow_msg, command.unallow_user(self.user)]

        return f"@{self.user} does not have permission to give: !{self.command}"
