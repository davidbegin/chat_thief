import pytest

from tests.support.database_setup import DatabaseConfig
from chat_thief.new_commands.buyer import Buyer
from chat_thief.new_commands.result import Result
from chat_thief.models.command import Command
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
        result = Buyer(user_with_points, "clap").buy()
        assert "clap" in User(user_with_points).commands()

    def test_buying_a_command_with_no_points(self):
        user = "fake_user"
        result = Buyer(user, "clap").buy()
        assert "clap" not in User(user).commands()

    def test_buying_a_random_command(self, user_with_points, mock_affordable_commands):
        Command("ohh").save()
        user = "fake_user"
        initial_cool_points = User(user).cool_points()
        result = Buyer(user, "random").buy()
        assert "clap" not in User(user_with_points).commands()
        assert User(user).cool_points() < initial_cool_points

    def test_buying_a_random_command_with_no_points(self):
        user = "fake_user"
        with pytest.raises(ValueError) as err:
            result = Buyer(user, "random").buy()

    def test_buying_multiple(self):
        user = User("fake_user")
        user.update_cool_points(100)
        result = Buyer(user.name, "random", 3).buy()
        purchase_results = result.metadata["purchase_results"]
        assert len(purchase_results) == 3

    def test_buying_a_random_command_with_syntax(
        self, user_with_points, mock_affordable_commands
    ):
        Command("ohh").save()
        user = "fake_user"
        initial_cool_points = User(user).cool_points()
        result = Buyer(user, "random").buy()
        assert "clap" not in User(user_with_points).commands()
        assert User(user).cool_points() < initial_cool_points

    def test_buying_same_command(self, user_with_points, mock_affordable_commands):
        user = User(user_with_points)
        assert len(user.commands()) == 0
        command = Command("mchdtmd").save()
        result = Buyer(user.name, command.name).buy()
        assert len(user.commands()) == 1
        result = Buyer(user.name, command.name).buy()
        assert len(user.commands()) == 1
