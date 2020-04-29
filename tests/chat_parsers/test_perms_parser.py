import pytest

from chat_thief.chat_parsers.perms_parser import PermsParser
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.models.user import User


class TestPermsParser:
    def test_parse(self, monkeypatch):
        def mockreturn(self):
            return ["artmattdank"]

        def fakecommands(self):
            return ["clap"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", mockreturn)
        monkeypatch.setattr(User, "commands", fakecommands)

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

        # This isn't
        # mocker.patch("WelcomeCommittee.present_users")
        # mocker.patch("chat_thief.welcome_committee")

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
