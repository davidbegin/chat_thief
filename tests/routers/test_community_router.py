import pytest

from chat_thief.models.command import Command
from chat_thief.models.proposal import Proposal
from chat_thief.models.sfx_vote import SFXVote
from chat_thief.models.user import User
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.routers.community_router import CommunityRouter
from chat_thief.welcome_committee import WelcomeCommittee

from tests.support.database_setup import DatabaseConfig


class TestCommunityRouter(DatabaseConfig):
    @pytest.fixture
    def mock_find_random_user(self, monkeypatch):
        def _fake_find_random_user(self):
            return "young.thug"

        monkeypatch.setattr(
            UserSoundeffectRouter, "_random_user", _fake_find_random_user
        )

    @pytest.fixture(autouse=True)
    def mock_present_users(self, monkeypatch):
        def _mock_present_users(self):
            return ["not_streamlord", "young.thug", "uzi"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", _mock_present_users)

    def test_propose(self):
        assert Proposal.count() == 0
        result = CommunityRouter(
            "beginbot", "propose", ["!iasip", "The", "Gang", "Steals", "Kappa"]
        ).route()
        assert result == "Thank you @beginbot for your proposal"
        last = Proposal.last()
        assert last["proposal"] == "The Gang Steals Kappa"
        assert last["command"] == "iasip"

    def test_iasip_propose(self):
        assert Proposal.count() == 0
        result = CommunityRouter(
            "beginbot", "iasip", ["The", "Gang", "Steals", "Kappa"]
        ).route()

        assert result == "Thank you @beginbot for your proposal"
        last = Proposal.last()
        assert last["proposal"] == "The Gang Steals Kappa"
        assert last["command"] == "iasip"

    # We want Proposals to only last 5 minutes
    def test_support(self):
        CommunityRouter.SUPPORT_REQUIREMENT = 1
        BreakingNews.count() == 0
        assert Proposal.count() == 0
        result = CommunityRouter(
            "beginbot", "propose", ["!iasip", "The", "Gang", "Steals", "Kappa"]
        ).route()
        result = CommunityRouter("uzi", "support", ["@beginbot"]).route()
        proposal = Proposal.last()
        assert proposal["proposed_at"] is not None
        assert result == "@beginbot thanks you for the support @uzi"
        assert BreakingNews.count() == 1

        proposal = Proposal("beginbot")
        # how can we look up the object???
        assert not proposal.is_expired()
        OG_EXPIRE_TIME = Proposal.EXPIRE_TIME_IN_SECS
        Proposal.EXPIRE_TIME_IN_SECS = 0
        assert proposal.is_expired()
        Proposal.EXPIRE_TIME_IN_SECS = OG_EXPIRE_TIME
