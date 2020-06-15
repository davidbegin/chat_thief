import pytest

from chat_thief.stats_department import StatsDepartment
from tests.support.database_setup import DatabaseConfig
from chat_thief.models.command import Command
from chat_thief.models.user import User

# - Total Unrealized wealth of sound effects
# - Total User Wealth


class TestStatsDepartment(DatabaseConfig):
    def test_stats(self):
        subject = StatsDepartment()
        stats = subject.stats()
        keys = stats.keys()

        assert stats["total_street_cred"] == 0
        assert stats["total_cool_points"] == 0
        assert stats["fed_reserve"] == 0
        assert stats["total_user_sfx_property"] == 0

        command = Command("damn")
        command.save()
        user = User("clams")
        command.allow_user("clams")
        user.set_value("street_cred", 50)
        user.set_value("cool_points", 10)

        stats = subject.stats()
        assert stats["total_street_cred"] == 50
        assert stats["total_cool_points"] == 10
        assert stats["fed_reserve"] == 0
        assert stats["total_user_sfx_property"] == 1
