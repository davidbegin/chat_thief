import pytest

from chat_thief.routers.basic_info_router import BasicInfoRouter
from tests.support.database_setup import DatabaseConfig


class TestBasicInfoRouter(DatabaseConfig):
    def test_la_libre(self):
        result = BasicInfoRouter("la_libre").route()
        assert result == [
            "PowerUpL La Libre PowerUpR",
            "Total Votes: 0",
            "Peace Count: 0 / 3",
            "Revolution Count: 0 / 3",
            "panicBasket Coup Cost: 1 panicBasket",
        ]

    def test_stream_gods_and_lords(self, monkeypatch):
        result = BasicInfoRouter("streamgods").route()
        assert result == "beginbot beginbotbot stupac62 artmattdank"
        result = BasicInfoRouter("streamlords").route()
        assert "zerostheory" in result
