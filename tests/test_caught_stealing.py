import pytest

from chat_thief.caught_stealing import CaughtStealing
from chat_thief.models.rap_sheet import RapSheet
from tests.support.database_setup import DatabaseConfig

import random


class TestCaughtStealing(DatabaseConfig):
    def test_people_get_caught_stealing(self):
        random.seed(1)
        thief = "uzi"
        target_sfx = "clap"
        assert CaughtStealing(thief, target_sfx, "future").call()
        rap_sheet = RapSheet.last()
        assert rap_sheet["user"] == "uzi"
        assert rap_sheet["metadata"] == {"target_sfx": "clap", "victim": "future"}

    def test_getting_caught(self):
        random.seed(0)
        thief = "uzi"
        target_sfx = "clap"
        assert not CaughtStealing(thief, target_sfx, "future").call()
