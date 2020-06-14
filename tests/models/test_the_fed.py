import pytest

from chat_thief.models.the_fed import TheFed
from chat_thief.models.command import Command

from tests.support.database_setup import DatabaseConfig


class TestTheFed(DatabaseConfig):
    def test_taxes(self):
        result = TheFed.reserve()
        assert result == 0

        command = Command("handbag")
        command.save()
        command.set_value("cost", 2)

        the_fed = TheFed
        the_fed.collect_taxes()

        result = TheFed.reserve()
        assert result == 1
        assert command.cost() == 1
