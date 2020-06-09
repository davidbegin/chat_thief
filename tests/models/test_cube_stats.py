from pathlib import Path

import pytest

from chat_thief.models.user import User
from chat_thief.models.cube_stats import CubeStats

from tests.support.database_setup import DatabaseConfig


class TestCubeStats(DatabaseConfig):
    def test_stats(self):
        winning_duration = 40
        winners = ["uzi"]
        all_bets = [("future", 21)]

        subject = CubeStats(
            winning_duration=winning_duration, winners=winners, all_bets=all_bets
        )
        assert CubeStats.count() == 0
        subject.save()
        assert CubeStats.count() == 1
