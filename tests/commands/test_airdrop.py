import pytest

from chat_thief.commands.airdrop import Airdrop
from chat_thief.models.user import User
from tests.support.database_setup import DatabaseConfig
from chat_thief.chat_logs import ChatLogs
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary


class TestAirDrop(DatabaseConfig):
    @pytest.fixture
    def mock_users(self, monkeypatch):
        def _mock_recent_stream_peasants(self):
            return ["thugga"]

        monkeypatch.setattr(
            ChatLogs, "recent_stream_peasants", _mock_recent_stream_peasants
        )

    @pytest.fixture
    def mock_soundeffects(self, monkeypatch):
        def _mock_soundeffects_only():
            return ["clap"]

        monkeypatch.setattr(
            SoundeffectsLibrary, "soundeffects_only", _mock_soundeffects_only
        )

    def test_with_no_args(self, mock_users, mock_soundeffects):
        subject = Airdrop()
        user = User("grant.green")
        assert subject.drop() == "@thugga now has access to Sound Effect: !clap"

    def test_with_target_user(self, mock_soundeffects):
        subject = Airdrop(target_user="future")
        user = User("grant.green")
        assert subject.drop() == "@future now has access to Sound Effect: !clap"

    def test_with_target_command(self, mock_users):
        subject = Airdrop(target_command="wassup")
        user = User("grant.green")
        assert subject.drop() == "@thugga now has access to Sound Effect: !wassup"

    def test_with_user_and_command(self):
        subject = Airdrop(target_user="wes", target_command="wassup")
        user = User("grant.green")
        assert subject.drop() == "@wes now has access to Sound Effect: !wassup"

    def test_with_just_amount(self, mock_users, mock_soundeffects):
        subject = Airdrop(amount=2)
        user = User("grant.green")
        result = subject.drop()
        assert result == [
            "@thugga now has access to Sound Effect: !clap",
            "@thugga now has access to Sound Effect: !clap",
        ]
        # assert result == "@thugga now has access to Sound Effect: !clap"

    def test_with_amount_and_user(self, mock_soundeffects):
        subject = Airdrop(target_user="ella", amount=2)
        user = User("grant.green")
        result = subject.drop()
        assert result == [
            "@ella now has access to Sound Effect: !clap",
            "@ella now has access to Sound Effect: !clap",
        ]

    def test_with_amount_and_command(self, mock_users):
        subject = Airdrop(target_command="handbag", amount=2)
        user = User("grant.green")
        result = subject.drop()
        assert result == [
            "@thugga now has access to Sound Effect: !handbag",
            "@thugga now has access to Sound Effect: !handbag",
        ]

    def test_with_amount_command_and_user(self):
        subject = Airdrop(target_user="ella", target_command="handbag", amount=2)
        user = User("grant.green")
        result = subject.drop()
        assert result == [
            "@ella now has access to Sound Effect: !handbag",
            "@ella now has access to Sound Effect: !handbag",
        ]
