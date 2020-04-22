import pytest

from chat_thief.chat_parsers.transfer_request_parser import TransferRequestParser

class TestTransferRequestParser:

    def test_parse(self):
        user = "fake_user"

        args = ["@IACCHUS", "clap"]
        subject = TransferRequestParser(user, args)
        result = subject.parse()
        assert result.target_user == "iacchus"
        assert result.target_command == "clap"
        assert result.transferer == user


        args = ["!clap", "@IACCHUS"]
        subject = TransferRequestParser(user, args)
        result = subject.parse()
        assert result.target_user == "iacchus"
        assert result.target_command == "clap"
        assert result.transferer == user
        # args = ["clap", "@iacchus"]
