import traceback
from typing import Optional

from dataclasses import dataclass

from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.soundeffects_library import SoundeffectsLibrary


@dataclass
class PropsRequest:
    target_user: Optional[str]
    requester: str
    amount: Optional[int] = 1


class PropsParser:
    def __init__(self, user, args=[]):
        self.user = user
        self.args = [ self._sanitize(arg) for arg in args ]

        self.target_user = None
        self.amount = 1
        self._set_target_user_and_amount()

    def parse(self):
        return PropsRequest(
            target_user=self.target_user,
            amount=self.amount,
            requester=self.user
        )

    def _set_target_user_and_amount(self):
        for arg in self.args:
            self._check_and_set(arg)

    def _check_and_set(self, arg):
        if self._is_user(arg):
            self.target_user = arg
        if self._is_valid_amount(arg):
            self.amount = int(arg)

    def _is_user(self, user):
        return user in WelcomeCommittee().present_users() or user == "random"

    def _is_valid_amount(self, val):
        try:
            return int(val) > 1
        except (Exception, ValueError):
            traceback.print_exc()
            return False

    def _sanitize(self, item):
        if item.startswith("!") or item.startswith("@"):
            return item[1:].lower()
        else:
            return item.lower()
