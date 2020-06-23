import pytest

from chat_thief.models.bot_vote import BotVote
from chat_thief.models.user import User
from chat_thief.routers.bot_survivor_router import BotSurvivorRouter
from tests.support.database_setup import DatabaseConfig


class TestBotSurviorRouter(DatabaseConfig):
    def test_voting_for_a_bot(self):
        User("uzibot").save()
        User.register_bot("uzibot", "don.cannon")
        result = BotSurvivorRouter("beginbotbot", "botvote", ["uzibot"]).route()

        assert BotVote.count() == 1
        assert result == "Thank you for your vote @beginbotbot"

    def test_try_to_vote_for_non_bot(self):
        User("uzibot_notbot").save()
        result = BotSurvivorRouter("beginbotbot", "botvote", ["uzibot_notbot"]).route()
        assert BotVote.count() == 0
        assert result == "@beginbotbot @uzibot_notbot is NOT A BOT!"

    def test_changing_your_vote(self):
        User("uzibot").save()
        User.register_bot("uzibot", "don.cannon")

        User("enobot").save()
        User.register_bot("enobot", "eno")

        result = BotSurvivorRouter("beginbotbot", "botvote", ["uzibot"]).route()
        assert BotVote.count() == 1
        assert result == "Thank you for your vote @beginbotbot"

        result = BotSurvivorRouter("beginbotbot", "botvote", ["enobot"]).route()
        assert BotVote.count() == 1
        assert result == "Thank you for your vote @beginbotbot"
