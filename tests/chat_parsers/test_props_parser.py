import pytest

from chat_thief.chat_parsers.props_parser import PropsParser
from chat_thief.welcome_committee import WelcomeCommittee


class TestPropsParser:
    def test_parse(self, monkeypatch):
        def fakeusers(self):
            return ["artmattdank"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", fakeusers)

        user = "fake_user"
        args = ["!props", "artmattDank"]
        subject = PropsParser(user, args)
        result = subject.parse()
        assert result.requester == user
        assert result.target_user == "artmattdank"
        assert result.requester == user
        assert result.amount == 1

        user = "fake_user"
        args = ["!props", "@artmattDank"]
        subject = PropsParser(user, args)
        result = subject.parse()
        assert result.target_user == "artmattdank"
        assert result.requester == user
        assert result.amount == 1

        user = "fake_user"
        args = ["!props", "@artmattDank", "10"]
        subject = PropsParser(user, args)
        result = subject.parse()
        assert result.target_user == "artmattdank"
        assert result.requester == user
        assert result.amount == 10
