import pytest

from chat_thief.commands.command_buyer import CommandBuyer
from chat_thief.models.command import Command
from chat_thief.models.user import User

from tests.support.database_setup import DatabaseConfig


class TestCommandBuyer(DatabaseConfig):
    @pytest.fixture
    def user_with_points(self):
        user = "fake_user"
        User("fake_user").update_cool_points(1)
        return user

    def test_buying_a_command(self, user_with_points):
        result = CommandBuyer(user_with_points, "clap").buy()
        assert result == f"@{user_with_points} bought !clap"
        assert "clap" in User(user_with_points).commands()

    def test_buying_a_command_with_no_points(self):
        user = "fake_user"
        Command("clap").increase_cost(3)
        result = CommandBuyer(user, "clap").buy()
        assert result == "@fake_user not enough Cool Points to buy !clap - 0/1"
        assert "clap" not in User(user).commands()
