import pytest
from pathlib import Path

from chat_thief.models.css_vote import CSSVote
from chat_thief.models.user import User
from chat_thief.models.user import Command
from tests.support.database_setup import DatabaseConfig


class TestCSSVote(DatabaseConfig):
    def _create_user(self, name):
        user = User(name=name)
        user._find_or_create_user()
        return user

    def test_its_real(self):
        assert CSSVote.count() == 0
        voter = "uzi"
        candidate = "future"
        CSSVote(voter=voter, candidate=candidate).save()
        assert CSSVote.count() == 1

    def test_by_votes(self):
        CSSVote(voter="uzi", candidate="future").save()
        CSSVote(voter="kanye", candidate="drake").save()
        CSSVote(voter="carti", candidate="future").save()
        result = CSSVote.by_votes()
        assert result == [
            ("future", 2),
            ("drake", 1),
        ]
