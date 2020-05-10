import pytest
from pathlib import Path

from chat_thief.models.cube_bet import CubeBet

from chat_thief.models.vote import Vote
from chat_thief.models.user import User
from chat_thief.models.user import Command
from tests.support.database_setup import DatabaseConfig


# Soon !bet
class TestCubeBet(DatabaseConfig):
    def _create_user(self, name):
        user = User(name=name)
        user._find_or_create_user()
        return user

    def test_betting(self):
        gambler = self._create_user("gucci.mane")
        duration = 26
        subject = CubeBet(gambler.name, duration)
        assert CubeBet.count() == 0
        subject.save()
        assert CubeBet.count() == 1
