import pytest

from chat_thief.data_scrubber import DataScrubber
from chat_thief.models.command import Command
from chat_thief.models.user import User

from tests.support.database_setup import DatabaseConfig


class TestDataScrubber(DatabaseConfig):
    def test_purge_theme_songs(self):
        uzi = User("uzi")
        illegal_cmd = Command("beginbot")
        illegal_cmd.save()
        illegal_cmd.allow_user("uzi")
        Command("damn").save()
        assert Command.count() == 2
        DataScrubber.purge_theme_songs()
        assert Command.count() == 1
        assert uzi.commands() == []

    def test_purge_duplicate_commands(self):
        uzi = User("uzi")
        illegal_cmd = Command("clap")
        illegal_cmd.permitted_users = ["uzi", "uzi"]
        illegal_cmd.save()

        illegal_cmd = Command("clap")
        illegal_cmd.permitted_users = ["uzi", "uzi"]
        illegal_cmd.save()
        assert Command.count() == 2

        DataScrubber.purge_duplicates()
        assert Command.count() == 1
        assert uzi.commands() == ["clap"]

    def test_purge_duplicate_users(self):
        uzi = User("uzi").save()
        uzi = User("uzi").save()
