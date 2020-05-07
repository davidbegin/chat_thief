import pytest

from chat_thief.commands.revolution import Revolution
from chat_thief.models.user import User
from chat_thief.models.vote import Vote
from chat_thief.models.command import Command
from tests.support.database_setup import DatabaseConfig


# We hide the Cost
class TestRevolution(DatabaseConfig):
    # Coup costs something, it doubles everytime
    # If you don't have the costs, you lose all you currency

    @pytest.fixture(autouse=True)
    def set_coup_price(self):
        self.coup = Command("coup")
        self.coup.save()
        self.coup.increase_cost(10)

    def test_attempt_coup_without_enough_cool_points(self):
        revolutionary = "beginbot"
        user = User(revolutionary)
        assert user.street_cred() == 0
        assert user.cool_points() == 0
        user.update_street_cred(1)
        user.update_cool_points(1)
        subject = Revolution(revolutionary)
        tide = Vote.have_tables_turned(1)
        result = subject.attempt_coup(tide)
        assert user.street_cred() == 0
        assert user.cool_points() == 0

    def test_attempt_coup_with_enough_cool_points(self):
        revolutionary = "beginbot"
        user = User(revolutionary)
        user.update_street_cred(1)
        user.update_cool_points(11)
        subject = Revolution(revolutionary)
        tide = Vote.have_tables_turned(1)
        subject.attempt_coup(tide)
        assert user.street_cred() == 1
        assert user.cool_points() == 0
        assert self.coup.cost() == 33

    def test_peace_keeper_losing_it_all(self):
        fence_sitter = User("CoolCat")
        fence_sitter.save()
        clap = Command("clap")
        clap.allow_user(fence_sitter.name)

        damn_command = Command("damn")
        peace_keeper = User("picakhu")
        damn_command.allow_user(peace_keeper.name)
        Vote(peace_keeper.name).vote("peace")
        assert peace_keeper.name in damn_command.users()

        revolutionary = User("beginbot")
        Vote(revolutionary.name).vote("revolution")
        revolutionary.update_cool_points(11)
        subject = Revolution(revolutionary.name)
        subject.attempt_coup("revolution")

        assert peace_keeper.name not in damn_command.users()
        assert revolutionary.name in damn_command.users()
        assert "damn" not in fence_sitter.commands()
        assert fence_sitter.name not in clap.users()
