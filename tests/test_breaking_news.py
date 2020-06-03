import pytest

# from breaking_news_bot_2 import BreakingNewsBot
# from chat_thief.bots.breaking_news_bot import BreakingNewsBot

from chat_thief.models.command import Command
from chat_thief.models.user import User
from chat_thief.models.breaking_news import BreakingNews

from tests.support.database_setup import DatabaseConfig


@pytest.mark.skip
class TestBreakingNewsBot(DatabaseConfig):
    def test_breaking_news_initialization(self):
        user = User("bill.evans")
        user.save()
        command = Command("damn")
        command.save()
        command.increase_cost(10)
        other_cmd = Command("win")
        other_cmd.save()
        subject = BreakingNewsBot()
        assert subject.in_coup == False
        assert subject.last_breaking_time == None
        assert subject.initial_most_expensive["name"] == "damn"
        assert subject.initial_richest_user["name"] == "bill.evans"

    def test_breaking_news(self):
        user = User("bill.evans")
        user.save()
        command = Command("damn")
        command.save()
        command.increase_cost(10)
        other_cmd = Command("win")
        other_cmd.save()
        subject = BreakingNewsBot()
        # how do we assert a method is called
        # assert subject.most_expensive_command == "Cool"
        # assert not subject.check_for_breaking_news()
        # BreakingNews("EVERYTHING IS BROKEN!").save()
        # assert subject.check_for_breaking_news()
