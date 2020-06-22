import pytest


from chat_thief.models.user import User
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
        assert "Thank you @beginbot for your proposal" in result
        last = Proposal.last()
        assert last["proposal"] == "The Gang Steals Kappa"
        assert last["command"] == "iasip"

    def test_iasip_propose(self):
        assert Proposal.count() == 0
        result = CommunityRouter(
            "beginbot", "iasip", ["The", "Gang", "Steals", "Kappa"]
        ).route()

        assert "Thank you @beginbot for your proposal" in result
        last = Proposal.last()
        assert last["proposal"] == "The Gang Steals Kappa"
        assert last["command"] == "iasip"

    def test_deleting_proposal_after_report(self):
        CommunityRouter.SUPPORT_REQUIREMENT = 1
        result = CommunityRouter(
            "beginbot", "propose", ["!iasip", "The", "Gang", "Steals", "Kappa"]
        ).route()
        Proposal.count() == 1
        result = CommunityRouter("uzi", "support", ["@beginbot"]).route()
        assert BreakingNews.count() == 1
        assert Proposal.count() == 0

    def test_support(self):
        CommunityRouter.SUPPORT_REQUIREMENT = 1
        BreakingNews.count() == 0
        assert Proposal.count() == 0
        result = CommunityRouter(
            "beginbot", "propose", ["!iasip", "The", "Gang", "Steals", "Kappa"]
        ).route()
        result = CommunityRouter("uzi", "support", ["@beginbot"]).route()
        assert result == "@beginbot Thanks You for the support @uzi 1/1"
        assert BreakingNews.count() == 1

    def test_support_last(self):
        CommunityRouter.SUPPORT_REQUIREMENT = 1
        result = CommunityRouter(
            "beginbot", "propose", ["!iasip", "The", "Gang", "Steals", "Kappa"]
        ).route()
        result = CommunityRouter("uzi", "support", []).route()
        assert "@beginbot Thanks You for the support @uzi" in result
        assert BreakingNews.count() == 1

    def test_top8(self):
        user = User("beginbot")
        User("uzi").save()

        result = CommunityRouter("beginbot", "top8", ["@uzi"]).route()
        assert result == "@uzi is now in @beginbot's Top 8!"
        assert user.top_eight() == ["uzi"]

        result = CommunityRouter("beginbot", "hate8", ["@uzi"]).route()
        assert result == "@uzi is no longer in @beginbot's Top 8"

        result = CommunityRouter("beginbot", "clear8", []).route()
        assert result == "@beginbot doesn't need friends, they disappoint them."
        assert user.top_eight() == []
