import pytest

from chat_thief.caught_stealing import CaughtStealing
from chat_thief.models.rap_sheet import RapSheet
from tests.support.database_setup import DatabaseConfig
from chat_thief.models.user import User

import random


class TestCaughtStealing(DatabaseConfig):
    def test_people_get_caught_stealing(self):
        random.seed(1)
        thief = "uzi"
        target_sfx = "clap"
        assert User("uzi").mana() == 3
        assert CaughtStealing(thief, target_sfx, "future").call()
        rap_sheet = RapSheet.last()
        assert User("uzi").mana() == 0
        assert rap_sheet["user"] == "uzi"
        assert rap_sheet["metadata"] == {"target_sfx": "clap", "victim": "future"}

    def test_not_getting_caught(self):
        random.seed(0)
        thief = "uzi"
        target_sfx = "clap"
        busted, percentage = CaughtStealing(thief, target_sfx, "future").call()
        assert not busted

    def test_huge_imbalance(self):
        pass
