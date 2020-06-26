import pytest

from chat_thief.models.bot_vote import BotVote
from chat_thief.models.tribal_council import TribalCouncil
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
        vote["user"] == "uzi"

    def test_create_or_update(self):
        assert BotVote.count() == 0
        result, update_type = BotVote("eno", "uzibot").create_or_update()
        assert BotVote.count() == 1
        assert update_type == "create"
        result, update_type = BotVote("eno", "otherbot").create_or_update()
        assert BotVote.count() == 1
        assert update_type == "update"

    def test_votes_by_bot(self):
        BotVote("eno", "uzibot").create_or_update()
        BotVote("future", "otherbot").create_or_update()
        BotVote("carti", "otherbot").create_or_update()
        result = BotVote.count_by_group("bot")
        assert result == [("otherbot", 2), ("uzibot", 1)]
