import pytest

from chat_thief.chat_logs import ChatLogs
from chat_thief.commands.la_libre import LaLibre, REVOLUTION_LIKELYHOOD
from chat_thief.models.vote import Vote
from chat_thief.models.command import Command
from chat_thief.models.user import User
from tests.support.database_setup import DatabaseConfig


class TestLaLibre(DatabaseConfig):
    def test_inform(self):
        Vote("fake_user").vote("peace")
        result = LaLibre.inform()
        self.coup = Command("coup")
        User("fake_user").save()

        peasants = ChatLogs().recent_stream_peasants()
        threshold = 3

        assert result == [
            "PowerUpL La Libre PowerUpR",
            "Total Votes: 1",
            f"Peace Count: 1 / {threshold}",
            f"Revolution Count: 0 / {threshold}",
            f"panicBasket Coup Cost: {self.coup.cost()} panicBasket",
        ]
