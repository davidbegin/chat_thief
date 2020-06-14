import pytest

from chat_thief.begin_fund import BeginFund
from chat_thief.models.the_fed import TheFed
from chat_thief.models.command import Command

from tests.support.database_setup import DatabaseConfig

class TestBeginFund(DatabaseConfig):
    def test_dropeffect(self):
        result = BeginFund().dropeffect()
        assert result == "The Fed is Broke"

        Command("damn", 2).save()
        Command("handbag", 10).save()
        TheFed.collect_taxes()
        assert TheFed.reserve() == 6

        result = BeginFund().dropeffect()
        assert "now has access" in result

    def test_dropping_specific_effects(self):
        Command("handbag", 10).save()
        TheFed.collect_taxes()
        assert TheFed.reserve() == 5
        result = BeginFund(target_user="uzi", target_command="damn").dropeffect()
        assert "@uzi now has access to the Soundeffect: !damn" in result
        assert TheFed.reserve() == 4

