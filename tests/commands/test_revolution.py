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
        assert (
            result
            == "@beginbot is now Bankrupt, that will teach you a lesson. Coups require 11 Cool Points"
        )

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

    def test_peace_scenario(self):
        fence_sitter = User("CoolCat")
        fence_sitter.save()
        clap_command = Command("clap")
        clap_command.allow_user(fence_sitter.name)
        fence_sitter.update_street_cred(10)
        fence_sitter.update_cool_points(10)

        peace_keeper = User("picakhu")
        damn_command = Command("damn")
        damn_command.allow_user(peace_keeper.name)
        Vote(peace_keeper.name).vote("peace")
        peace_keeper.update_cool_points(11)
        peace_keeper.update_street_cred(10)
        peace_keeper.update_cool_points(10)

        peace_keeper2 = User("beginbotsmonster")
        wassup_command = Command("wassup_command")
        wassup_command.allow_user(peace_keeper2.name)
        Vote(peace_keeper2.name).vote("peace")

        revolutionary = User("beginbot")
        listen_command = Command("listen")
        listen_command.allow_user(revolutionary.name)
        Vote(revolutionary.name).vote("revolution")

        subject = Revolution(peace_keeper.name)
        subject.attempt_coup("peace")

        assert peace_keeper.name in listen_command.users()
        assert peace_keeper2.name not in listen_command.users()
        assert revolutionary.name not in listen_command.users()
        assert fence_sitter.name not in clap_command.users()
        assert fence_sitter.street_cred() == 10
        assert fence_sitter.cool_points() == 10

    def test_revolution_scenario(self):
        fence_sitter = User("CoolCat")
        fence_sitter.update_street_cred(10)
        fence_sitter.update_cool_points(10)
        fence_sitter.save()
        clap_command = Command("clap")
        clap_command.allow_user(fence_sitter.name)

        peace_keeper = User("picakhu")
        peace_keeper.update_street_cred(10)
        peace_keeper.update_cool_points(10)
        damn_command = Command("damn")
        damn_command.allow_user(peace_keeper.name)
        another_one_command = Command("anotherone")
        another_one_command.allow_user(peace_keeper.name)
        Vote(peace_keeper.name).vote("peace")

        revolutionary2 = User("beginbotsmonster")
        wassup_command = Command("wassup")
        wassup_command.allow_user(revolutionary2.name)
        Vote(revolutionary2.name).vote("revolution")

        revolutionary = User("beginbot")
        listen_command = Command("listen")
        listen_command.allow_user(revolutionary.name)
        Vote(revolutionary.name).vote("revolution")
        revolutionary.update_cool_points(11)

        subject = Revolution(revolutionary.name)
        subject.attempt_coup("revolution")

        assert peace_keeper.name not in damn_command.users()
        assert revolutionary2.name in damn_command.users()
        assert revolutionary.name in another_one_command.users()

        assert revolutionary.name in listen_command.users()
        assert revolutionary2.name not in listen_command.users()
        assert fence_sitter.name not in clap_command.users()

        assert fence_sitter.street_cred() == 0
        assert fence_sitter.cool_points() == 0
        assert peace_keeper.street_cred() == 0
        assert peace_keeper.cool_points() == 0
