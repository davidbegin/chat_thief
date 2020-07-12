import pytest

from chat_thief.models.command import Command
from chat_thief.models.user import User
from chat_thief.models.breaking_news import BreakingNews
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.routers.moderator_router import ModeratorRouter
from tests.support.database_setup import DatabaseConfig
from chat_thief.chat_logs import ChatLogs


class TestModeratorRouter(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def mock_present_users(self, monkeypatch):
        def _mock_present_users(self):
            return ["future", "uzi"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", _mock_present_users)

    def test_silence(self):
        user = User("future")
        assert user.mana() == 3
        result = ModeratorRouter("beginbotbot", "silence", ["@future"]).route()
        assert user.mana() == 0

    def test_revive(self):
        user = User("future")
        ModeratorRouter("beginbotbot", "silence", ["@future"]).route()
        assert user.mana() == 0
        result = ModeratorRouter("beginbotbot", "revive", ["@future"]).route()
        assert user.mana() == 3

    def test_do_over(self):
        command = Command("damn")
        command.save()
        command.increase_cost(9)
        user = User("future", 100)
        user.save()
        assert user.cool_points() == 100
        result = ModeratorRouter("beginbotbot", "do_over", ["@future"]).route()
        assert command.cost() == 5
        assert result == "Society now must rebuild"

    def test_no_news(self):
        BreakingNews("Arch Linux is now Illegal").save()
        assert BreakingNews.count() == 1
        ModeratorRouter("beginbotbot", "no_news", []).route()
        assert BreakingNews.count() == 0

    def test_dropeffects(self, monkeypatch):
        monkeypatch.setattr(
            ChatLogs, "recent_stream_peasants", ["quavo: nice", "takeoff: IDK"]
        )
        result = ModeratorRouter("beginbotbot", "dropeffect").route()
        assert "now has access to" in result
