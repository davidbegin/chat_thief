import pytest
from pathlib import Path

from chat_thief.models.user_page import UserPage
from chat_thief.models.user import User
from chat_thief.models.user import Command
from tests.support.database_setup import DatabaseConfig


class TestUserPage(DatabaseConfig):
    def test_its_real(self):
        assert UserPage.count() == 0

        UserPage.bootstrap_user_page(user="eno", widgets=["bubbles"])

        result = UserPage.last()
        assert result["widgets"] == {"bubbles": True}

    def test_deactivating(self):
        UserPage.bootstrap_user_page(user="eno", widgets=["bubbles"])
        result = UserPage.deactivate("eno", "bubbles")
        user_page = UserPage.last()
        assert user_page["widgets"] == {"bubbles": False}

    def test_for_user(self):
        UserPage.bootstrap_user_page(user="eno", widgets=["bubbles"])
        user_page = UserPage.for_user("eno")
        assert user_page["widgets"] == {"bubbles": True}
