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

    def test_add_street_cred(self, user):
        subject = user("artmattdank")
        assert subject.street_cred() == 0
        subject.add_street_cred()
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
        subject.add_street_cred(10)
        subject.add_cool_points(10)
        assert subject.cool_points() == 10
        assert subject.street_cred() == 10
        subject.bankrupt()
        assert subject.cool_points() == 0
        assert subject.street_cred() == 0

    def test_count(self, user):
        subject = user("artmattdank")
        assert User.count() == 0
        subject.save()
        assert User.count() == 1

    def test_all(self, user):
        assert User.all() == []
        user("artmattdank").save()
        assert User.all() == ["artmattdank"]
        user("shiva").save()
        assert User.all() == ["artmattdank", "shiva"]

    def test_richest(self, user):
        subject = user("artmattdank")
        subject.add_cool_points(10)
        thugga = user("thugga")
        thugga.add_cool_points(3)
        otheruser = user("otheruser")
        otheruser.add_cool_points(5)
        result = User.richest()
        expected = [["thugga", 3], ["otheruser", 5], ["artmattdank", 10]]
        assert result == expected

    def test_total_cool_points(self, user):
        assert User.total_cool_points() == 0
        user("artmattdank").add_cool_points(10)
        assert User.total_cool_points() == 10
        user("artmattdank").add_cool_points(3)
        assert User.total_cool_points() == 13
        user("brianeno").add_cool_points(420)
        assert User.total_cool_points() == 433

    def test_total_street_cred(self, user):
        assert User.total_street_cred() == 0
        user("artmattdank").add_street_cred(10)
        assert User.total_street_cred() == 10
        user("artmattdank").add_street_cred(3)
        assert User.total_street_cred() == 13
        user("brianeno").add_street_cred(420)
        assert User.total_street_cred() == 433
