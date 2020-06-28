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
        ).save()

        last = UserCode.last()
        assert last["approved"] == False
        assert last["name"] == "beginwidget"
        assert last["owners"] == []

        assert UserCode.owned_by("eno") == ["beginwidget.js"]
        assert UserCode.find_owners("beginwidget") == [
            "eno",
        ]

        result = UserCode.purchase("begin", "beginwidget")
        assert UserCode.find_owners("beginwidget") == ["eno", "begin"]

    def test_extracing_name_from_url(self):
        UserCode(
            user="eno", code_link="https://gitlab.com/real_url/raw", code_type="js",
        ).save()

        last = UserCode.last()
        assert last["approved"] == False
        assert last["name"] == "eno"
        assert last["owners"] == []

        assert UserCode.owned_by("eno") == ["eno.js"]
