import pytest
from chat_thief.routers.user_soundeffect_router import UserSoundeffectRouter
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models.command import Command
from chat_thief.models.sfx_vote import SFXVote

from tests.support.database_setup import DatabaseConfig


class TestUserSoundeffectRouter(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def mock_present_users(self, monkeypatch):
        def _mock_present_users(self):
            return ["not_streamlord"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", _mock_present_users)

    def test_me(self):
        result = UserSoundeffectRouter("beginbotbot", "me", []).route()
        assert result == "@beginbotbot - Mana: 3 | Street Cred: 0 | Cool Points: 0"

    def test_perms(self):
        result = UserSoundeffectRouter("beginbotbot", "perms", ["clap"]).route()
        assert result == "!clap | Cost: 1 | Health: 0 | Like Ratio 100%"

    def test_donate(self):
        Command("clap").allow_user("thugga")
        assert "thugga" in Command("clap").users()
        result = UserSoundeffectRouter("thugga", "donate", []).route()
        assert "thugga" not in Command("clap").users()
        assert "was gifted" in result[0]

    def test_hate_and_like_command(self):
        assert SFXVote("clap").supporter_count() == 0
        assert SFXVote("clap").detractor_count() == 0
        result = UserSoundeffectRouter("thugga", "like", ["clap"]).route()
        assert SFXVote("clap").supporter_count() == 1
        result = UserSoundeffectRouter("future", "hate", ["clap"]).route()
        assert SFXVote("clap").detractor_count() == 1
