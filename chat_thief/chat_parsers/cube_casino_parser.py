import random
from typing import Optional

from dataclasses import dataclass

from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.prize_dropper import random_soundeffect
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models.user import User


@dataclass
class CubeCasinoRequest:
    user: str
    bet: Optional[int]
    wager: Optional[list]


class CubeCasinoParser:
    def __init__(self, user, command, args=[]):
        self.user = user
        self.args = [self._sanitize(arg) for arg in args]

    def parse(self):
        self._set_bet_and_wager()

        return CubeCasinoRequest(user=self.user, bet=self.bet, wager=self.wager)

    def _set_bet_and_wager(self):
        self.bet = 1
        self.wager = []

        for arg in self.args:
            if arg in SoundeffectsLibrary.soundeffects_only():
                self.wager.append(arg)

            if self._is_valid_bet(arg):
                if isinstance(arg, int):
                    self.bet = arg
                elif arg.endswith("s"):
                    self.bet = int(arg[:-1])
                else:
                    self.bet = int(arg)

    def _is_valid_bet(self, val):
        try:
            if isinstance(val, int):
                return val > 1
            elif val.endswith("s"):
                return int(val[:-1]) > 1
            else:
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
