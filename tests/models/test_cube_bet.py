import pytest
from pathlib import Path

from chat_thief.models.cube_bet import CubeBet

from chat_thief.models.vote import Vote
from chat_thief.models.user import User
from chat_thief.models.user import Command
from tests.support.database_setup import DatabaseConfig


class TestCubeBet(DatabaseConfig):
    def _create_user(self, name):
        user = User(name=name)
        user._find_or_create_user()
        return user

    def test_betting(self):
        name = self._create_user("gucci.mane")
        duration = 29
        subject = CubeBet(name.name, duration)
        assert CubeBet.count() == 0
        subject.save()
        assert CubeBet.count() == 1

        subject = CubeBet(name.name, 38)
        subject.save()

        assert CubeBet.count() == 1
        assert subject.duration() == 38

    def test_all_bets(self):
        result = CubeBet.all_bets()
        assert result == []
        CubeBet("carti", 32).save()
        result = CubeBet.all_bets()
        assert result == [("carti", 32, [])]
        CubeBet("uzi", 24).save()
        result = CubeBet.all_bets()
        assert result == [("uzi", 24, []), ("carti", 32, [])]

    def test_a_wager(self):
        result = CubeBet("carti", 32, ["clap"]).save()
        assert result.wager == ["clap"]
