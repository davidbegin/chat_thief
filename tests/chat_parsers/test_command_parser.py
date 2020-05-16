import pytest

from chat_thief.chat_parsers.command_parser import CommandParser
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models.user import User


class TestCommandParser:
    @pytest.fixture(autouse=True)
    def mock_present_users(self, monkeypatch):
        def _mock_present_users(self):
            return ["artmattdank", "fake_viewer"]

        def _mock_fake_commands(self):
            return ["clap"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", _mock_present_users)
        monkeypatch.setattr(User, "commands", _mock_fake_commands)

    def test_basic_parse(self):
        user = "fake_user"
        args = ["!perms", "clap"]
        subject = CommandParser(user, args)
        result = subject.parse()
        assert result.target_user == None
        assert result.target_command == "perms"
        assert result.target_sfx == "clap"
        assert result.requester == user

    def test_just_a_command(self):
        user = "fake_user"
        args = ["!perms", "!clap"]
        subject = CommandParser(user, args)
        result = subject.parse()
        assert result.target_user == None
        assert result.target_command == "perms"
        assert result.target_sfx == "clap"
        assert result.requester == user

    def test_just_a_user(self):
        user = "fake_user"
        args = ["!perms", "@artmattDank"]
        subject = CommandParser(user, args)
        result = subject.parse()
        assert result.target_user == "artmattdank"
        assert result.target_command == "perms"
        assert result.target_sfx == None
        assert result.requester == user

    def test_a_buy_random_command(self):
        user = "beginbotbot"
        args = ["!buy", "random"]
        subject = CommandParser(user, args, allow_random_sfx=True)
        result = subject.parse()
        assert result.target_user == None
        assert result.target_command == "buy"
        assert result.target_sfx == "random"
        assert result.requester == user

    def test_a_buy_random_command_when_not_allowed(self):
        user = "beginbotbot"
        args = ["!buy", "random"]
        subject = CommandParser(user, args, allow_random_sfx=False)
        result = subject.parse()
        assert result.target_user == None
        assert result.target_command == "buy"
        assert result.target_sfx == None
        assert result.requester == user

    def test_a_give_random_command(self):
        user = "beginbotbot"
        args = ["!give", "@artmattDank", "random"]
        subject = CommandParser(user, args, allow_random_sfx=True)
        result = subject.parse()
        assert result.target_user == "artmattdank"
        assert result.target_command == "give"
        assert result.target_sfx == "random"
        assert result.requester == user

    def test_transfer_to_random_user(self):
        user = "beginbotbot"
        args = ["!transfer", "random", "random"]
        subject = CommandParser(
            user, args, allow_random_sfx=True, allow_random_user=True
        )
        result = subject.parse()
        assert result.target_user == "random"
        assert result.target_command == "transfer"
        assert result.target_sfx == "random"
        assert result.requester == user

    def test_transfer_to_random_user_when_not_allowed(self):
        user = "fake_user"
        args = ["!transfer", "random", "random"]
        subject = CommandParser(
            user, args, allow_random_sfx=True, allow_random_user=False
        )
        result = subject.parse()
        assert result.target_user == None
        assert result.target_command == "transfer"
        assert result.target_sfx == "random"
        assert result.requester == user

    def test_transfer_to_random_command(self):
        user = "fake_user"
        args = ["!transfer", "random", "random"]
        subject = CommandParser(
            user, args, allow_random_sfx=False, allow_random_user=True
        )
        result = subject.parse()
        assert result.target_user == "random"
        assert result.target_command == "transfer"
        assert result.target_sfx == None
        assert result.requester == user

    def test_transfer(self):
        user = "fake_user"
        args = ["!transfer", "@artmattdank", "!clap"]
        subject = CommandParser(user, args)
        result = subject.parse()
        assert result.target_user == "artmattdank"
        assert result.target_command == "transfer"
        assert result.target_sfx == "clap"
        assert result.requester == user
