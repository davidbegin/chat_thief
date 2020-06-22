import pytest

from chat_thief.models.bot_vote import BotVote
from chat_thief.models.tribal_council import TribalCouncil
from chat_thief.models.user import User
from tests.support.database_setup import DatabaseConfig


class TestTribalCouncil(DatabaseConfig):
    def test_bot_vote(self):
        TribalCouncil.count() == 0
        uzi = User("uzi")
        bot = User("uzibot")
        BotVote(user=uzi.name, bot=bot.name).save()
        assert BotVote.count() == 1
        vote = BotVote.last()
        vote["bot"] == "uzibot"
        vote["user"] == "uzi"

        TribalCouncil.go_to_tribal()

        assert TribalCouncil.count() == 1
        vote = TribalCouncil.last()
        assert vote == {"council_number": 1, "votes": {"uzibot": ["uzi"]}}

        BotVote(user=uzi.name, bot="pattymartinobot").save()
        TribalCouncil.go_to_tribal()
        assert TribalCouncil.count() == 2
        vote = TribalCouncil.last()
        assert vote == {"council_number": 2, "votes": {"pattymartinobot": ["uzi"]}}
