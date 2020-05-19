import pytest

from chat_thief.routers.revolution_router import RevolutionRouter
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models.vote import Vote
from tests.support.database_setup import DatabaseConfig


class TestRevolutionRouter(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def mock_present_users(self, monkeypatch):
        def _mock_present_users(self):
            return ["future", "uzi"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", _mock_present_users)

    # Should we move our "acceptance" test here
    def test_coup(self):
        result = RevolutionRouter("beginbotbot", "coup", []).route()
        assert (
            result
            == "The Will of the People have not chosen: 3 votes must be cast for either Peace or Revolution"
        )

    def test_vote(self):
        assert Vote.count() == 0
        result = RevolutionRouter("beginbotbot", "vote", ["peace"]).route()
        assert Vote.count() == 1
