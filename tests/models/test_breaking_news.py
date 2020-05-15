import pytest

from chat_thief.models.breaking_news import BreakingNews
from tests.support.database_setup import DatabaseConfig


class TestBreakingNews(DatabaseConfig):
    def test_breaking_news(self):
        subject = BreakingNews(
            scope="Cool Points are now the most valuable currency in the world!"
        )
        assert BreakingNews.count() == 0
        subject.save()
        assert BreakingNews.count() == 1

    def test_breaking_news_with_user(self):
        subject = BreakingNews(
            scope="Cool Points are now the most valuable currency in the world!",
            user="coltrane",
        )

        assert subject._user == "coltrane"

    def test_breaking_news_with_category(self):
        subject = BreakingNews(
            scope="Cool Points are now the most valuable currency in the world!",
            user="coltrane",
            category="coup",
        )
        subject.save()

        news = BreakingNews.all()[-1]

        assert news["user"] == "coltrane"
        assert news["category"] == "coup"
