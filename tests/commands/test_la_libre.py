import pytest

from chat_thief.commands.la_libre import LaLibre
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

        threshold = int(User.count() / 10)

        # Who are people who trigger the coup?
        # people who have at least the coup costs

        assert result == [
            "PowerUpL La Libre PowerUpR",
            "Total Votes: 1",
            "Peace Count: 1",
            "Revolution Count: 0",
            f"Votes Required: {threshold}",
            f"panicBasket Coup Cost: {self.coup.cost()} panicBasket",
        ]
