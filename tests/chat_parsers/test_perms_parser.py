import pytest

from chat_thief.chat_parsers.perms_parser import PermsParser
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models.user import User


class TestPermsParser:
    @pytest.fixture(autouse=True)
    def mock_present_users(self, monkeypatch):
        def _mock_present_users(self):
            return ["artmattdank", "fake_viewer"]

        def _mock_fake_commands(self):
            return ["clap"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", _mock_present_users)
        monkeypatch.setattr(User, "commands", _mock_fake_commands)

    def test_parse(self):
        user = "fake_user"
        args = ["!perms", "clap"]
        subject = PermsParser(user, args)
        result = subject.parse()
        assert result.target_user == None
        assert result.target_command == "clap"
        assert result.requester == user

        user = "fake_user"
        args = ["!perms", "!clap"]
        subject = PermsParser(user, args)
        result = subject.parse()
        assert result.target_user == None
        assert result.target_command == "clap"
        assert result.requester == user

        user = "fake_user"
        args = ["!perms", "@artmattDank"]
        subject = PermsParser(user, args)
        result = subject.parse()

        assert result.target_user == "artmattdank"
        assert result.target_command == None
        assert result.requester == user

        user = "beginbotbot"
        args = ["!give", "@artmattDank", "random"]
        subject = PermsParser(user, args, random_command=True)
        result = subject.parse()
        assert result.target_user == "artmattdank"
        assert result.target_command != None
        assert result.target_command != "random"
        assert result.requester == user

        user = "beginbotbot"
        args = ["!give", "@artmattDank", "random"]
        subject = PermsParser(user, args, random_command=True)
        result = subject.parse()
        assert result.target_user == "artmattdank"
        assert result.target_command != None
        assert result.target_command != "random"
        assert result.requester == user

    def test_give_parse(self):
        user = "fake_user"
        args = ["!give", "unusual", "fake_viewer"]
        subject = PermsParser(user, args, random_command=True, random_user=True,)
        result = subject.parse()
        assert result.target_command == "unusual"
        assert result.target_user == "fake_viewer"

        args = ["!give", "fake_viewer", "unusual"]
        subject = PermsParser(user, args)
        result = subject.parse()
        assert result.target_command == "unusual"
        assert result.target_user == "fake_viewer"
