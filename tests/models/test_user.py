from pathlib import Path

import pytest

from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.models.sfx_vote import SFXVote

from tests.support.database_setup import DatabaseConfig


class TestUser(DatabaseConfig):
    def test_commands(self):
        subject = User("artmattdank")
        assert User.count() == 1
        assert subject.commands() == []
        command = Command("flacid")
        command.allow_user("artmattdank")
        assert command.users() == ["artmattdank"]
        assert subject.commands() == ["flacid"]

    def test_update_street_cred(self):
        subject = User("artmattdank")
        assert subject.street_cred() == 0
        subject.update_street_cred(1)
        assert subject.street_cred() == 1

    @pytest.mark.skip
    def test_remove_all_commands(self):
        subject = User("artmattdank")
        assert subject.commands() == []
        command = Command("flacid")
        command.allow_user("artmattdank")
        assert command.permitted_users() == ["artmattdank"]
        assert subject.commands() == ["flacid"]
        subject.remove_all_commands()
        assert subject.commands() == []
        assert command.permitted_users() == []

    def test_bankrupt(self):
        subject = User("artmattdank")
        subject.update_street_cred(10)
        subject.update_cool_points(10)
        assert subject.cool_points() == 10
        assert subject.street_cred() == 10
        subject.bankrupt()
        assert subject.cool_points() == 0
        assert subject.street_cred() == 0

    def test_richest(self):
        subject = User("artmattdank")
        subject.update_cool_points(10)
        thugga = User("thugga")
        thugga.update_cool_points(3)
        otheruser = User("otheruser")
        otheruser.update_cool_points(5)
        result = User.richest()
        expected = [("thugga", 3), ("otheruser", 5), ("artmattdank", 10)]
        assert result == expected

    def test_total_cool_points(self):
        assert User.total_cool_points() == 0
        User("artmattdank").update_cool_points(10)
        assert User.total_cool_points() == 10
        User("artmattdank").update_cool_points(3)
        assert User.total_cool_points() == 13
        User("brianeno").update_cool_points(420)
        assert User.total_cool_points() == 433

    def test_total_street_cred(self):
        assert User.total_street_cred() == 0
        User("artmattdank").update_street_cred(10)
        assert User.total_street_cred() == 10
        User("artmattdank").update_street_cred(3)
        assert User.total_street_cred() == 13
        User("brianeno").update_street_cred(420)
        assert User.total_street_cred() == 433

    def test_total_cool_points(self):
        assert User.total_cool_points() == 0
        User("artmattdank").update_cool_points(-10)
        assert User.total_cool_points() == -10
        User("artmattdank").update_cool_points(-3)
        assert User.total_cool_points() == -13
        User("brianeno").update_cool_points(-420)
        assert User.total_cool_points() == -433

    def test_removing_street_cred(self):
        assert User.total_street_cred() == 0
        User("artmattdank").update_street_cred(-10)
        assert User.total_street_cred() == -10
        User("artmattdank").update_street_cred(-3)
        assert User.total_street_cred() == -13
        User("brianeno").update_street_cred(-420)
        assert User.total_street_cred() == -433

    def test_mana(self):
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

    def test_karma(self):
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

    def test_richest_cool_points(self):
        User.richest_cool_points() == None
        watto = User("watto", 3)
        artmattdank = User("artmattdank", 9)

        tpain = User("tpain", 1)
        tpain.update_cool_points(1)
        User.richest_cool_points()["name"] == "artmattdank"
        assert User.wealthiest() == "artmattdank"

    def test_custom_css(self):
        lahey = User("lahey")
        custom_css = "https://gist.githubusercontent.com/raw/d7bcdf8"
        lahey.set_value("custom_css", custom_css)
        assert lahey.custom_css() == custom_css

    def test_top_eight(self):
        uzi = User("uzi")
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

    def test_total_wealth(self):
        subject = User("bill.evans")
        assert subject.top_wealth() == 0
        subject.update_cool_points(1)
        assert subject.top_wealth() == 1
        command = Command("damn")
        command.allow_user("bill.evans")
        assert subject.top_wealth() == 2
        command.set_value("cost", 10)
        assert subject.top_wealth() == 11

    def test_wealthiest(self):
        subject = User("bill.evans", 1)
        command = Command("damn")
        command.allow_user("bill.evans")
        command.set_value("cost", 10)
        assert User.wealthiest() == "bill.evans"

    def test_wealth(self):
        subject = User("bill.evans")
        subject.update_cool_points(11)
        command = Command("damn", 10)
        command.allow_user("bill.evans")
        assert subject.wealth() == 21

    # @pytest.mark.skip
    def test_is_bot(self):
        creator = "bill.evans"
        bot = User("bill.evans.bot")
        User.register_bot(bot=bot.name, creator=creator)
        User.bots() == ["bill.evans.bot"]

        assert bot.is_bot()
        assert bot.creator() == "bill.evans"

    def test_insured(self):
        subject = User("snorlax")
        assert not subject.insured()
        result = subject.buy_insurance()
        assert result == "YA Broke @snorlax - it costs 1 Cool Point to buy insurance"
        assert not subject.insured()
        subject.update_cool_points(1)
        result = subject.buy_insurance()
        assert result == "@snorlax thank you for purchasing insurance"
        assert subject.insured()
