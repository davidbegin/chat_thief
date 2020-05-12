import pytest

from chat_thief.commands.airdrop import Airdrop
from chat_thief.models.user import User
from tests.support.database_setup import DatabaseConfig
from chat_thief.chat_logs import ChatLogs
from chat_thief.soundeffects_library import SoundeffectsLibrary


class TestAirDrop(DatabaseConfig):
    @pytest.fixture
    def mock_stream_peasants(self, monkeypatch):
        def _mock_recent_stream_peasants(self):
            return ["thugga"]

        def _mock_soundeffects_only():
            return ["clap"]

        monkeypatch.setattr(
            ChatLogs, "recent_stream_peasants", _mock_recent_stream_peasants
        )
        monkeypatch.setattr(
            SoundeffectsLibrary, "soundeffects_only", _mock_soundeffects_only
        )

    def test_with_no_args(self, mock_stream_peasants):
        subject = Airdrop()
        user = User("grant.green")
        assert subject.drop() == "@thugga now has access to Sound Effect: !clap"

    # no args
    # target_user, target_command
    # target_command
    # target_user
    # amount
    # target_user amount
    # target_command amount
