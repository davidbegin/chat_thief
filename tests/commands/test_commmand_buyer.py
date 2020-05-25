import pytest

from chat_thief.commands.command_buyer import CommandBuyer
from chat_thief.models.command import Command
from chat_thief.models.user import User

from tests.support.database_setup import DatabaseConfig


class TestCommandBuyer(DatabaseConfig):
    @pytest.fixture
    def mock_affordable_commands(self, monkeypatch):
        def _fake_affordable_commands(self):
            return Command("ohh")

        monkeypatch.setattr(
            User, "_find_affordable_random_command", _fake_affordable_commands
        )

    @pytest.fixture
    def user_with_points(self):
        user = "fake_user"
        User("fake_user").update_cool_points(1)
        return user

    def test_buying_a_command(self, user_with_points):
        result = CommandBuyer(user_with_points, "clap").buy()
        assert result == f"@{user_with_points} bought !clap for 1 Cool Points"
        assert "clap" in User(user_with_points).commands()

    def test_buying_a_command_with_no_points(self):
        user = "fake_user"
        result = CommandBuyer(user, "clap").buy()
        assert result == "@fake_user not enough Cool Points to buy !clap - 0/1"
        assert "clap" not in User(user).commands()

    def test_buying_a_random_command(self, user_with_points, mock_affordable_commands):
        Command("ohh").save()
        user = "fake_user"
        initial_cool_points = User(user).cool_points()
        result = CommandBuyer(user, "random").buy()
        assert result == f"@{user_with_points} bought !ohh for 1 Cool Points"
        assert "clap" not in User(user_with_points).commands()
        assert User(user).cool_points() < initial_cool_points

    def test_buying_a_random_command_with_no_points(self):
        user = "fake_user"
        with pytest.raises(ValueError) as err:
            result = CommandBuyer(user, "random").buy()
