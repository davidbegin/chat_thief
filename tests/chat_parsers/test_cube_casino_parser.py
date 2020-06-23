import pytest

from chat_thief.chat_parsers.cube_casino_parser import CubeCasinoParser
from chat_thief.models.user import User

from tests.support.database_setup import DatabaseConfig


class TestCommandParser(DatabaseConfig):
    def test_parsing_multiple_targets(self):
        user = "eno"
        args = ["45", "clap", "damn"]
        subject = CubeCasinoParser(user, "bet", args)
        result = subject.parse()
        assert result.wager == ["clap", "damn"]
        assert result.bet == 45
        assert result.user == user
