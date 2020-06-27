import pytest

from chat_thief.models.bot_vote import BotVote
from chat_thief.models.user import User
from chat_thief.routers.bot_survivor_router import BotSurvivorRouter
from tests.support.database_setup import DatabaseConfig


class TestBotSurviorRouter(DatabaseConfig):
    def test_voting_for_a_bot(self):
        User("uzibot", 1)
        result = User.register_bot("uzibot", "don.cannon")
        result = BotSurvivorRouter("beginbotbot", "hatebot", ["uzibot"]).route()

        assert BotVote.count() == 1
        assert result == "Thank you for your vote @beginbotbot"

    def test_try_to_vote_for_non_bot(self):
        User("uzibot_notbot").save()
        result = BotSurvivorRouter("beginbotbot", "hatebot", ["uzibot_notbot"]).route()
        assert BotVote.count() == 0
        assert result == "@beginbotbot @uzibot_notbot is NOT A BOT!"

    def test_changing_your_vote(self):
        User.register_bot("uzibot", "don.cannon")
        User.register_bot("enobot", "eno")

        result = BotSurvivorRouter("beginbotbot", "hatebot", ["uzibot"]).route()
        assert BotVote.count() == 1
        assert result == "Thank you for your vote @beginbotbot"

        result = BotSurvivorRouter("beginbotbot", "hatebot", ["enobot"]).route()
        assert BotVote.count() == 1
        assert result == "Thank you for your vote @beginbotbot"

    def test_tribal_council(self):
        User.register_bot("uzibot", "don.cannon")
        User.register_bot("enobot", "eno")

        BotVote("beginbotbot", "uzibot").save()
        BotVote("future", "uzibot").save()
        BotVote("carti", "enobot").save()
        assert BotVote.count() == 3

        result = BotSurvivorRouter("beginbotbot", "tribal_council", []).route()
        assert result == "@uzibot has been kicked out of BeginWorld"
