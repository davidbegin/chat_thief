import random
from typing import Optional

from dataclasses import dataclass

from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.prize_dropper import random_soundeffect
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models.user import User


@dataclass
class PermsRequest:
    target_user: Optional[str]
    target_command: Optional[str]
    requester: str


# Permission Type
class PermsParser:
    def __init__(
        self, user, args=[], random_user=False, random_command=False, perm_type="give"
    ):
        self.user = user
        self.args = [self._sanitize(arg) for arg in args]
        self.random_user = random_user
        self.random_command = random_command
        self.perm_type = perm_type

        self.target_user = None
        self.target_command = None
        self._set_target_user_and_command()

    def parse(self):
        if self.target_command == "random":
            if self.perm_type == "buy":
                from chat_thief.prize_dropper import random_soundeffect

                command = random_soundeffect()
            elif self.perm_type in ["give", "transfer", "share"]:
                # If someone tries to give a a random sample
                # they need a sample
                command = random.sample(User(self.user).commands(), 1)[0]
            self.target_command = command

        if self.target_user == "random":
            from chat_thief.prize_dropper import random_user

            self.target_user = random_user()

        return PermsRequest(
            target_user=self.target_user,
            target_command=self.target_command,
            requester=self.user,
        )

    def _set_target_user_and_command(self):
        for arg in self.args:
            self._check_and_set(arg)

    def _check_and_set(self, arg):
        if self._is_user(arg):
            self.target_user = arg

        if self._is_command(arg):
            self.target_command = arg

    def _is_command(self, command):
        if self.random_command:
            return (
                command in SoundeffectsLibrary.fetch_soundeffect_names()
                or command == "random"
            )
        else:
            return command in SoundeffectsLibrary.soundeffects_only()

    def _is_user(self, user):
        if user in STREAM_GODS:
            return True
        elif self.random_user:
            return user in WelcomeCommittee().present_users() or user == "random"
        else:
            return user in WelcomeCommittee().present_users()

    def _sanitize(self, item):
        if item.startswith("!") or item.startswith("@"):
            return item[1:].lower()
        else:
            return item.lower()
