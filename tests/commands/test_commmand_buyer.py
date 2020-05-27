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
        result = CommandBuyer(user_with_points, "clap").new_buy()
        assert f"@{user_with_points} bought 1 SFXs:" in result
        assert "clap" in User(user_with_points).commands()

    def test_buying_a_command_with_no_points(self):
        user = "fake_user"
        result = CommandBuyer(user, "clap").new_buy()
        assert "clap" not in User(user).commands()
        assert result == "@fake_user not enough Cool Points to buy !clap - 0/1"

    def test_buying_a_random_command(self, user_with_points, mock_affordable_commands):
        Command("ohh").save()
        user = "fake_user"
        initial_cool_points = User(user).cool_points()
        result = CommandBuyer(user, "random").new_buy()
        assert f"@{user_with_points} bought 1 SFXs:" in result
        assert "clap" not in User(user_with_points).commands()
        assert User(user).cool_points() < initial_cool_points

    def test_buying_a_random_command_with_no_points(self):
        user = "fake_user"
        with pytest.raises(ValueError) as err:
            result = CommandBuyer(user, "random").new_buy()

    def test_buying_multiple(self):
        user = User("fake_user")
        user.update_cool_points(100)
        result = CommandBuyer(user.name, "random", 3).new_buy()
        assert "@fake_user bought 3 SFXs:" in result

    def test_buying_a_random_command_with_syntax(
        self, user_with_points, mock_affordable_commands
    ):
        Command("ohh").save()
        user = "fake_user"
        initial_cool_points = User(user).cool_points()
        result = CommandBuyer(user, "random").new_buy()
        assert f"@{user_with_points} bought 1 SFXs:" in result
        assert "clap" not in User(user_with_points).commands()
        assert User(user).cool_points() < initial_cool_points
