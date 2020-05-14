import pytest

from chat_thief.models.breaking_news import BreakingNews
from tests.support.database_setup import DatabaseConfig


class TestBreakingNews(DatabaseConfig):
    def test_breaking_new(self):
        subject = BreakingNews(
            scope="Cool Points are now the most valuable currency in the world!"
        )
        assert BreakingNews.count() == 0
        subject.save()
        assert BreakingNews.count() == 1
