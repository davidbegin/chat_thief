import pytest

from chat_thief.chat_parsers.transfer_request_parser import TransferRequestParser

class TestTransferRequestParser:

    def test_parse(self):
        user = "fake_user"

        args = ["@artmattdank", "clap"]
        subject = TransferRequestParser(user, args)
        result = subject.parse()
        assert result.target_user == "artmattdank"
        assert result.target_command == "clap"
        assert result.transferer == user


        args = ["!clap", "@ARTMATTDANK"]
        subject = TransferRequestParser(user, args)
        result = subject.parse()
        assert result.target_user == "artmattdank"
        assert result.target_command == "clap"
        assert result.transferer == user
