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
        user.add_street_cred(1)
        user.add_cool_points(1)
        subject = Revolution(revolutionary)
        tide = Vote.have_tables_turned(1)
        result = subject.attempt_coup(tide)
        assert user.street_cred() == 0
        assert user.cool_points() == 0

    def test_attempt_coup_with_enough_cool_points(self):
        revolutionary = "beginbot"
        user = User(revolutionary)
        user.add_street_cred(1)
        user.add_cool_points(11)
        subject = Revolution(revolutionary)
        tide = Vote.have_tables_turned(1)
        subject.attempt_coup(tide)
        assert user.street_cred() == 1
        assert user.cool_points() == 0
        assert self.coup.cost() == 33

    def test_peace_keeper_losing_it_all(self):
        damn_command = Command("damn")
        peace_keeper = "picakhu"
        damn_command.allow_user(peace_keeper)
        Vote(peace_keeper).vote("peace")
        assert peace_keeper in damn_command.users()

        revolutionary = "beginbot"
        user = User(revolutionary)
        Vote(revolutionary).vote("revolution")
        user.add_cool_points(11)
        subject = Revolution(revolutionary)
        subject.attempt_coup("revolution")

        assert peace_keeper not in damn_command.users()
        assert revolutionary in damn_command.users()
