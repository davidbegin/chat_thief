import random
from typing import Optional

from dataclasses import dataclass

from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.prize_dropper import random_soundeffect
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models.user import User


@dataclass
class CommandRequest:
    target_user: Optional[str]
    target_command: Optional[str]
    target_sfx: Optional[str]
    requester: str
    amount: Optional[int]


class CommandParser:
    def __init__(
        self, user, command, args=[], allow_random_user=False, allow_random_sfx=False
    ):
        self.user = user
        self.target_command = command
        self.args = [self._sanitize(arg) for arg in args]
        self.allow_random_user = allow_random_user
        self.allow_random_sfx = allow_random_sfx

    def parse(self):
        self._set_target_user_and_command()

        return CommandRequest(
            target_user=self.target_user,
            target_command=self.target_command,
            target_sfx=self.target_sfx,
            requester=self.user,
            amount=self.amount,
        )

    def _set_target_user_and_command(self):
        self.target_user = None
        self.target_sfx = None
        self.amount = 1

        for arg in self.args:
            if self._is_user(arg):
                self.target_user = arg

            if self._is_sfx(arg):
                self.target_sfx = arg

            if self._is_valid_amount(arg):
                self.amount = int(arg)

        if self.target_sfx is None and self.target_user is None:
            if len(self.args) == 0:
                if self.allow_random_user:
                    self.target_user = "random"
                if self.allow_random_sfx:
                    self.target_sfx = "random"

    def _is_sfx(self, sfx):
        if self.allow_random_sfx and sfx == "random":
            return True

        return sfx in SoundeffectsLibrary.soundeffects_only()

    def _is_user(self, user):
        if user in ["beginbot", "beginbotbot"]:
            return True
        elif user in STREAM_GODS:
            return True
        elif self.allow_random_user:
            return user in WelcomeCommittee().present_users() or user == "random"
        else:
            return user in WelcomeCommittee().present_users()

    def _is_valid_amount(self, val):
        try:
            return int(val) > 1
        except (Exception, ValueError):
            return False

    def _sanitize(self, item):
        if isinstance(item, int):
            return item
        elif item.startswith("!") or item.startswith("@"):
            return item[1:].lower()
        else:
            return item.lower()
