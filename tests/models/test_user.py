from pathlib import Path

import pytest

from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.models.sfx_vote import SFXVote

from tests.support.database_setup import DatabaseConfig


class TestUser(DatabaseConfig):
    @pytest.fixture
    def user(self):
        def _user(name):
            return User(name=name)

        return _user

    def test_commands(self, user):
        subject = user("artmattdank")
        assert subject.commands() == []
        command = Command("flacid")
        command.allow_user("artmattdank")
        assert command.users() == ["artmattdank"]
        assert subject.commands() == ["flacid"]

    def test_update_street_cred(self, user):
        subject = user("artmattdank")
        assert subject.street_cred() == 0
        subject.update_street_cred(1)
        assert subject.street_cred() == 1

    @pytest.mark.skip
    def test_remove_all_commands(self, user):
        subject = user("artmattdank")
        assert subject.commands() == []
        command = Command("flacid")
        command.allow_user("artmattdank")
        assert command.permitted_users() == ["artmattdank"]
        assert subject.commands() == ["flacid"]
        subject.remove_all_commands()
        assert subject.commands() == []
        assert command.permitted_users() == []

    def test_bankrupt(self, user):
        subject = user("artmattdank")
        subject.update_street_cred(10)
        subject.update_cool_points(10)
        assert subject.cool_points() == 10
        assert subject.street_cred() == 10
        # subject.bankrupt()
        # assert subject.cool_points() == 0
        # assert subject.street_cred() == 0

    def test_count(self, user):
        assert User.count() == 0
        subject = user("artmattdank")
        assert User.count() == 1

    def test_all(self, user):
        assert User.all() == []
        user("artmattdank").save()
        assert User.all() == ["artmattdank"]
        user("shiva").save()
        assert User.all() == ["artmattdank", "shiva"]

    def test_richest(self, user):
        subject = user("artmattdank")
        subject.update_cool_points(10)
        thugga = user("thugga")
        thugga.update_cool_points(3)
        otheruser = user("otheruser")
        otheruser.update_cool_points(5)
        result = User.richest()
        expected = [["thugga", 3], ["otheruser", 5], ["artmattdank", 10]]
        assert result == expected

    def test_total_cool_points(self, user):
        assert User.total_cool_points() == 0
        user("artmattdank").update_cool_points(10)
        assert User.total_cool_points() == 10
        user("artmattdank").update_cool_points(3)
        assert User.total_cool_points() == 13
        user("brianeno").update_cool_points(420)
        assert User.total_cool_points() == 433

    def test_total_street_cred(self, user):
        assert User.total_street_cred() == 0
        user("artmattdank").update_street_cred(10)
        assert User.total_street_cred() == 10
        user("artmattdank").update_street_cred(3)
        assert User.total_street_cred() == 13
        user("brianeno").update_street_cred(420)
        assert User.total_street_cred() == 433

    def test_total_cool_points(self, user):
        assert User.total_cool_points() == 0
        user("artmattdank").update_cool_points(-10)
        assert User.total_cool_points() == -10
        user("artmattdank").update_cool_points(-3)
        assert User.total_cool_points() == -13
        user("brianeno").update_cool_points(-420)
        assert User.total_cool_points() == -433

    def test_removing_street_cred(self, user):
        assert User.total_street_cred() == 0
        user("artmattdank").update_street_cred(-10)
        assert User.total_street_cred() == -10
        user("artmattdank").update_street_cred(-3)
        assert User.total_street_cred() == -13
        user("brianeno").update_street_cred(-420)
        assert User.total_street_cred() == -433

    def test_mana(self, user):
        subject = User("artmattdank")
        assert subject.mana() == 3
        subject.kill()
        assert subject.mana() == 0
        subject.revive()
        assert subject.mana() == 3
        subject.update_mana(-1)
        assert subject.mana() == 2
        subject.revive()
        assert subject.mana() == 3

    def test_karma(self, user):
        subject = User("gary")
        other_user = User("ash")
        assert subject.karma() == 0
        other_user.set_ride_or_die(subject.name)
        assert subject.karma() == 1

        another_user = User("meowth")
        another_user.set_ride_or_die(subject.name)
        assert subject.karma() == 2

        other_user.set_ride_or_die(another_user.name)
        assert subject.karma() == 1

    def test_setting_ride_or_die_to_self(self):
        subject = User("gary")
        subject.set_ride_or_die("gary")
        assert subject.karma() == 0

    def test_richest_street_cred(self):
        User.richest_street_cred() == None
        watto = User("watto")
        watto.save()
        watto.update_street_cred(3)

        artmattdank = User("artmattdank")
        artmattdank.save()
        artmattdank.update_street_cred(9)

        tpain = User("tpain")
        tpain.save()
        tpain.update_street_cred(1)
        User.richest_street_cred()["name"] == "artmattdank"

    def test_richest_cool_points(self):
        User.richest_cool_points() == None
        watto = User("watto")
        watto.save()
        watto.update_cool_points(3)
        artmattdank = User("artmattdank")
        artmattdank.save()
        artmattdank.update_cool_points(9)

        tpain = User("tpain")
        tpain.save()
        tpain.update_cool_points(1)
        User.richest_cool_points()["name"] == "artmattdank"

        result = [user["name"] for user in User.top_three()]
        assert result == ["artmattdank", "watto", "tpain"]

    def test_buy(self):
        watto = User("watto")
        watto.save()
        watto.update_cool_points(3)
        result = watto.buy("clap")
        assert result == "@watto bought !clap for 1 Cool Points"
        assert watto.cool_points() < 3

    def test_all_data(self):
        baldclap = User("baldclap")
        baldclap.save()
        baldclap.update_cool_points(3)
        Command("damn").allow_user("baldclap")
        custom_css = "https://gist.githubusercontent.com/davidbegin/efdbf338ecfcdc14fa9ed792c6056ed3/raw/d7bcdf2f3c9ae4b3e280646601061b0b4de3a2c8/beginfun"
        baldclap.set_value("custom_css", custom_css)
        all_data = User.all_data()

        assert all_data == [
            {
                "name": "baldclap",
                "command_file": "baldclap.opus",
                "street_cred": 0,
                "cool_points": 3,
                "mana": 3,
                "notoriety": 0,
                "custom_css": custom_css,
                "commands": ["damn"],
                "top_eight": [],
            }
        ]

    def test_custom_css(self, user):
        lahey = user("lahey")
        custom_css = "https://gist.githubusercontent.com/davidbegin/efdbf338ecfcdc14fa9ed792c6056ed3/raw/d7bcdf2f3c9ae4b3e280646601061b0b4de3a2c8/beginfun"
        lahey.set_value("custom_css", custom_css)
        assert lahey.custom_css() == custom_css

    def test_top_eight(self, user):
        uzi = user("uzi")
        assert uzi.top_eight() == []

        uzi.add_to_top_eight("playboi.carti")
        assert uzi.top_eight() == ["playboi.carti"]
        uzi.add_to_top_eight("playboi.carti")
        assert uzi.top_eight() == ["playboi.carti"]

        uzi.remove_from_top_eight("playboi.carti")
        assert uzi.top_eight() == []
        uzi.remove_from_top_eight("playboi.carti")
        assert uzi.top_eight() == []

        for x in range(0, 8):
            uzi.add_to_top_eight(f"user_{x}")

        with pytest.raises(ValueError) as err:
            uzi.add_to_top_eight("one_too_many")

        uzi.clear_top_eight()
        assert uzi.top_eight() == []

    def test_total_wealth(self, user):
        subject = user("bill.evans")
        assert subject.top_wealth() == 0
        subject.update_cool_points(1)
        assert subject.top_wealth() == 1
        command = Command("damn")
        command.allow_user("bill.evans")
        assert subject.top_wealth() == 2
        command.set_value("cost", 10)
        assert subject.top_wealth() == 11

    def test_wealthiest(self, user):
        subject = user("bill.evans")
        subject = user("sammy.davis")
        subject.update_cool_points(1)
        command = Command("damn")
        command.allow_user("bill.evans")
        command.set_value("cost", 10)
        assert User.wealthiest() == "bill.evans"

    def test_notoriety(self, user):
        subject = user("lilb")
        subject.notoriety() == 0

    def test_wealth(self, user):
        subject = user("bill.evans")
        subject.update_cool_points(11)
        command = Command("damn", 10)
        command.allow_user("bill.evans")
        assert subject.wealth() == 21
