import pytest

from chat_thief.routers.voting_booth_router import VotingBoothRouter
from chat_thief.models.user import User
from chat_thief.models.css_vote import CSSVote

from tests.support.database_setup import DatabaseConfig


class FakeParser:
    def __init__(self, target_user="coltrane"):
        self.target_user = target_user


class TestVotingBoothRouter(DatabaseConfig):
    def test_best_css(self):
        User("uzi").save()
        result = VotingBoothRouter("future", "bestcss", ["uzi"]).route()
        assert CSSVote.count() == 1

    def test_homepage(self):
        User("uzi").save()
        CSSVote(voter="don.cannon", candidate="rich.the.kid",).save()
        CSSVote(voter="uzi", candidate="future",).save()
        CSSVote(voter="carti", candidate="future",).save()
        result = VotingBoothRouter("future", "homepage", []).route()
        assert result == "@future: 2 | @rich.the.kid: 1"
