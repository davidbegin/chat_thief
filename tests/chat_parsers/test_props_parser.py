import pytest

from chat_thief.chat_parsers.props_parser import PropsParser


class TestPropsParser:
    def test_parse(self):
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
