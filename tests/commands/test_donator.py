import pytest

from chat_thief.commands.donator import Donator

from chat_thief.models.user import User
from chat_thief.models.command import Command

from tests.support.database_setup import DatabaseConfig


class TestDonator(DatabaseConfig):
    def test_donate(self):
        user = User("uzi")
        Command("clap").allow_user(user.name)
        Command("damn").allow_user(user.name)
        assert "uzi" in Command("clap").users()
        assert "uzi" in Command("damn").users()
        assert "young.thug" not in Command("clap").users()
        assert "young.thug" not in Command("damn").users()
        result = Donator(user.name).donate("young.thug")
        assert "young.thug" in Command("clap").users()
        assert "young.thug" in Command("damn").users()
        assert "uzi" not in Command("clap").users()
        assert "uzi" not in Command("damn").users()
        assert result == "@young.thug was gifted !clap !damn"

    def test_you_cannot_donate_your_theme(self):
        user = User("uzi")
        Command("clap").allow_user(user.name)
        Command("uzi").allow_user(user.name)
        assert "uzi" in Command("clap").users()
        assert "uzi" in Command("uzi").users()
        assert "young.thug" not in Command("clap").users()
        assert "young.thug" not in Command("uzi").users()
        result = Donator(user.name).donate("young.thug")
        assert "young.thug" in Command("clap").users()
        assert "young.thug" not in Command("uzi ").users()
        assert "uzi" not in Command("clap").users()
        assert result == "@young.thug was gifted !clap"
