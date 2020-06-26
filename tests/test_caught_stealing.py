import pytest

from chat_thief.caught_stealing import CaughtStealing
from chat_thief.models.rap_sheet import RapSheet
from chat_thief.models.user_event import UserEvent
from tests.support.database_setup import DatabaseConfig
from chat_thief.models.user import User

import random


class TestCaughtStealing(DatabaseConfig):
    def test_people_get_caught_stealing(self):
        random.seed(1)  # 17 from randint(0, 100)
        thief = "uzi"
        target_sfx = "clap"
        assert User("uzi").mana() == 3
        busted, percentage = CaughtStealing(thief, target_sfx, "future").call()
        assert not busted
        assert User("uzi").mana() == 3

        # rap_sheet = RapSheet.last()
        # assert rap_sheet["user"] == "uzi"
        # assert rap_sheet["metadata"] == {"target_sfx": "clap", "victim": "future"}

    def test_not_getting_caught(self):
        random.seed(5)  # 79 from randint(0, 100)
        thief = "uzi"
        target_sfx = "clap"
        busted, percentage = CaughtStealing(thief, target_sfx, "future").call()
        assert busted

    def test_huge_imbalance(self):
        pass

    def test_giving_and_stealing_and_5_percent(self):
        random.seed(5)  # 79 from randint(0, 100)
        thief = "uzi"
        target_sfx = "clap"
        victim = User("future")
        victim.save()

        busted, percentage = CaughtStealing(
            thief, target_sfx, "future", steal_count=2, give_count=0
        ).call()
        assert percentage == 40

        busted, percentage = CaughtStealing(
            thief, target_sfx, "future", steal_count=20, give_count=0
        ).call()
        assert percentage == 0

        busted, percentage = CaughtStealing(
            thief, target_sfx, "future", steal_count=20, give_count=40
        ).call()
        assert percentage == 70

        victim.update_cool_points(10)
        busted, percentage = CaughtStealing(
            thief, target_sfx, "future", steal_count=20, give_count=40
        ).call()
        assert percentage == 60

        victim.update_cool_points(1000)
        busted, percentage = CaughtStealing(
            thief, target_sfx, "future", steal_count=0, give_count=0
        ).call()
        assert percentage == 30
