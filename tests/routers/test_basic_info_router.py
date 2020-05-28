import pytest

from chat_thief.routers.basic_info_router import BasicInfoRouter
from chat_thief.models.user import User
from chat_thief.chat_parsers.command_parser import CommandParser

from tests.support.database_setup import DatabaseConfig


class FakeParser:
    def __init__(self, target_user="coltrane"):
        self.target_user = target_user


class TestBasicInfoRouter(DatabaseConfig):
    def test_la_libre(self):
        result = BasicInfoRouter("billy", "la_libre").route()
        assert result == " | ".join(
            [
                "PowerUpL La Libre PowerUpR",
                "Total Votes: 0",
                "Peace Count: 0 / 3",
                "Revolution Count: 0 / 3",
                "panicBasket Coup Cost: 1 panicBasket",
            ]
        )

    def test_stream_gods_and_lords(self, monkeypatch):
        result = BasicInfoRouter("sammy", "streamgods").route()
        assert "stupac62" in result
        result = BasicInfoRouter("sammy", "streamlords").route()
        assert "zerostheory" in result

    def test_shoutout(self):
        result = BasicInfoRouter("thugga", "so", ["beginbot"]).route()
        assert result == "Shoutout twitch.tv/beginbot"
        result = BasicInfoRouter("thugga", "so", ["$beginbot"]).route()
        assert result == "Shoutout twitch.tv/%24beginbot"
        result = BasicInfoRouter("thugga", "so", ["@beginbot"]).route()
        assert result == "Shoutout twitch.tv/beginbot"

    def test_bankrupt(self, monkeypatch):
        user = User("coltrane")
        user.update_cool_points(10)
        user.update_street_cred(10)

        def _fake_parse(self):
            return FakeParser()

        monkeypatch.setattr(CommandParser, "parse", _fake_parse)

        result = BasicInfoRouter("beginbotbot", "bankrupt", ["coltrane"]).route()
        assert user.cool_points() == 0
        assert user.street_cred() == 0
        assert result == "@coltrane is now Bankrupt"

    def test_paperup(self, monkeypatch):
        user = User("coltrane")

        def _fake_parse(self):
            return FakeParser()

        monkeypatch.setattr(CommandParser, "parse", _fake_parse)

        result = BasicInfoRouter("beginbotbot", "paperup", ["coltrane"]).route()
        assert user.cool_points() == 100
        assert user.street_cred() == 100
        assert result == "@coltrane has been Papered Up"

    def test_paperup_no_one(self, monkeypatch):
        def _fake_parse(self):
            return FakeParser(None)

        monkeypatch.setattr(CommandParser, "parse", _fake_parse)

        result = BasicInfoRouter("beginbotbot", "paperup", []).route()
        assert result == "You need to specify who to Paperup"
