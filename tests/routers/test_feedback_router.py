import pytest

from chat_thief.models.soundeffect_request import SoundeffectRequest
from chat_thief.routers.feedback_router import FeedbackRouter

from tests.support.database_setup import DatabaseConfig

# FeedbackRouter is not a good name
# these are commands that users submit
# and a Streamlord approves later on
class TestFeedbackRouter(DatabaseConfig):
    def test_requesting_sfx(self):
        result = FeedbackRouter(
            "beginbotbot",
            "soundeffect",
            ["VW2yff3su0U", "storm_seeker", "00:01", "00:04"],
        ).route()
        assert SoundeffectRequest.count() == 1

    # def test_approving_sfx
    # def test_denying_sfx
    # def submitting_issue
    # def delete_issue
