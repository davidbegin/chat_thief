import pytest

from chat_thief.bots.breaking_news_bot import BreakingNewsBot

from tests.support.database_setup import DatabaseConfig


class TestBreakingNewsBot(DatabaseConfig):
    def test_breaking_news(self):
        subject = BreakingNewsBot()
        assert subject.in_coup == False
