import pytest

from chat_thief.models.bot_vote import BotVote
from chat_thief.models.user import User
from tests.support.database_setup import DatabaseConfig


class TestBotVote(DatabaseConfig):
    def test_bot_vote(self):
        BotVote.count() == 0
        uzi = User("uzi")
        bot = User("uzibot")
        BotVote(user=uzi.name, bot=bot.name).save()
        vote = BotVote.last()
        vote["bot"] == "uzibot"

        assert "uzibot" == BotVote.vote_off_bot()
