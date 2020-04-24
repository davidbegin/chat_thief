from typing import Optional

from dataclasses import dataclass

from chat_thief.welcome_file import WelcomeFile
from chat_thief.soundeffects_library import SoundeffectsLibrary


@dataclass
class PermsRequest:
    target_user: Optional[str]
    target_command: Optional[str]
    requester: str


class PermsParser:
    def __init__(self, user, args=[]):
        self.user = user
        self.args = [ self._sanitize(arg) for arg in args ]

        self.target_user = None
        self.target_command = None
        self._set_target_user_and_command()

    def parse(self):
        return PermsRequest(
            target_user=self.target_user,
            target_command=self.target_command,
            requester=self.user
        )

    def _set_target_user_and_command(self):
        for arg in self.args:
            self._check_and_set(arg)

    def _check_and_set(self, arg):
        if self._is_user(arg):
            self.target_user = arg
        elif self._is_command(arg):
            self.target_command = arg

    def _is_command(self, command):
        return command in SoundeffectsLibrary.fetch_soundeffect_names()

    def _is_user(self, user):
        return user in WelcomeFile.present_users()

    def _sanitize(self, item):
        if item.startswith("!") or item.startswith("@"):
            return item[1:].lower()
        else:
            return item.lower()
