import pytest

from chat_thief.chat_parsers.perms_parser import PermsParser

class TestPermsParser:

    @pytest.mark.focus
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
