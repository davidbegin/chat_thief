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


        # ["!perms", "artmattdank"]
        # ["!perms", "!clap"]
        # ["!perms", "@artmattdank"]
        # args = ["!clap", "@ARTMATTDANK"]
        # subject = TransferRequestParser(user, args)
        # result = subject.parse()
        # assert result.target_user == "artmattdank"
        # assert result.target_command == "clap"
        # assert result.transferer == user
