import pytest

from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.routers.feedback_router import FeedbackRouter
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models.issue import Issue

from tests.support.database_setup import DatabaseConfig

# FeedbackRouter is not a good name
# these are commands that users submit
# and a Streamlord approves later on
class TestFeedbackRouter(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def mock_present_users(self, monkeypatch):
        def _mock_present_users(self):
            return ["not_streamlord"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", _mock_present_users)

    def test_requesting_sfx(self):
        result = FeedbackRouter(
            "beginbotbot",
            "soundeffect",
            ["VW2yff3su0U", "storm_seeker", "00:01", "00:04"],
        ).route()
        assert SoundeffectRequest.count() == 1

    # We must mock out the WelcomeCommittee
    def test_approving_sfx(self, mock_present_users):
        result = FeedbackRouter(
            "not_streamlord",
            "soundeffect",
            ["VW2yff3su0U", "storm_seeker", "00:01", "00:04"],
        ).route()
        assert SoundeffectRequest.count() == 1
        result = FeedbackRouter("beginbotbot", "approve", ["not_streamlord"]).route()
        assert SoundeffectRequest.count() == 0

    def test_denying_sfx(self, mock_present_users):
        result = FeedbackRouter(
            "not_streamlord",
            "soundeffect",
            ["VW2yff3su0U", "storm_seeker", "00:01", "00:04"],
        ).route()
        assert SoundeffectRequest.count() == 1
        result = FeedbackRouter("beginbotbot", "deny", ["not_streamlord"]).route()
        assert SoundeffectRequest.count() == 0

    def test_submitting_and_deleting_issue(self):
        assert Issue.count() == 0
        result = FeedbackRouter(
            "not_streamlord", "issue", ["THIS THING DOESN'T WORK"],
        ).route()
        assert Issue.count() == 1
        result = FeedbackRouter("beginbotbot", "issues").route()
        assert result == ["@not_streamlord ID: 1 - THIS THING DOESN'T WORK"]
        FeedbackRouter("beginbotbot", "delete_issue", ["not_streamlord"],).route()
        assert Issue.count() == 0
