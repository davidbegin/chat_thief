import pytest

from tests.support.database_setup import DatabaseConfig
from chat_thief.new_commands.buyer import Buyer
from chat_thief.new_commands.result import Result
from chat_thief.models.user import User


class TestBuyer(DatabaseConfig):
    def test_buying(self):
        subject = Buyer(user="madonna", target_sfx="handbag")
        user = User("madonna")
        user.set_value("cool_points", 1)
        result = subject.buy()

        assert isinstance(result, Result)
        assert result.user == "madonna"
        assert result.command == "buy"
        assert "handbag" in user.commands()
        assert result.cool_points_diff == -1
