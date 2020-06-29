import pytest

from chat_thief.models.user_code import UserCode
from chat_thief.models.user import User
from tests.support.database_setup import DatabaseConfig


class TestUserCode(DatabaseConfig):
    def test_user_code(self):
        assert UserCode.count() == 0

        UserCode(
            user="eno",
            code_link="https://gitlab.com/real_url/beginwidget.js",
            code_type="js",
            approved=True,
        ).save()

        last = UserCode.last()
        assert last["approved"] == True
        assert last["name"] == "beginwidget"
        assert last["owners"] == []

        assert UserCode.owned_by("eno") == ["beginwidget.js"]

        assert UserCode.find_owners("beginwidget") == [
            "eno",
        ]

        result = UserCode.purchase("begin", "beginwidget")
        assert UserCode.find_owners("beginwidget") == ["eno", "begin"]
        assert UserCode.owned_by("begin") == ["beginwidget.js"]

    def test_extracing_name_from_url(self):
        UserCode(
            user="eno", code_link="https://gitlab.com/real_url/raw", code_type="js",
        ).save()

        last = UserCode.last()
        assert last["approved"] == False
        assert last["name"] == "eno"
        assert last["owners"] == []

        assert UserCode.owned_by("eno") == ["eno.js"]

    def test_owned_by(self):
        UserCode(
            user="eno",
            code_link="https://gitlab.com/real_url/raw/bubbles.js",
            code_type="js",
            approved=False,
        ).save()

        assert UserCode.owned_by("eno") == ["bubbles.js"]

    def test_dev_leaderboard(self):
        UserCode(
            user="eno",
            code_link="https://gitlab.com/real_url/raw/bubbles.js",
            code_type="js",
            owners=["future"],
            approved=True,
        ).save()

        result = UserCode.dev_leaderboard()
        assert result == {"eno": 1}

    def test_widgets_for_user(self):
        UserCode(
            user="eno",
            code_link="https://gitlab.com/real_url/raw/bubbles.js",
            code_type="js",
            owners=["future"],
            approved=True,
        ).save()

        UserCode(
            user="uzi",
            code_link="https://gitlab.com/real_url/raw/fun.js",
            code_type="js",
            owners=["future"],
            approved=False,
        ).save()

        result = UserCode.js_for_user("future")
        assert result == {"approved": ["bubbles.js"], "unapproved": ["fun.js"]}
