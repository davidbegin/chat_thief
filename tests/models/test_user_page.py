import pytest
from pathlib import Path

from chat_thief.models.user_page import UserPage
from chat_thief.models.user import User
from chat_thief.models.user import Command
from tests.support.database_setup import DatabaseConfig


class TestUserPage(DatabaseConfig):
    def test_its_real(self):
        assert UserPage.count() == 0

        UserPage(
            user="eno",
            widgets=["bubbles"]
        ).save()

        result = UserPage.last()
        assert result["widgets"] == {
            "bubbles": True
        }

    def test_deactivating(self):
        UserPage(
            user="eno",
            widgets=["bubbles"]
        ).save()
        result = UserPage.deactivate("eno", "bubbles")
        user_page = UserPage.last()
        assert user_page["widgets"] == {
            "bubbles": False
        }
