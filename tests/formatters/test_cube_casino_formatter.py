import pytest

from chat_thief.formatters.cube_casino_formatter import CubeCasinoFormatter

from tests.support.database_setup import DatabaseConfig


class TestCubeCasinoFormatter(DatabaseConfig):
    def test_a_solved_cube(self):
        winners = [
            ("uzi", "ella", "hello"),
            ("uzi", "future", "damn"),
            ("eno", "ella", "8bitrickroll"),
        ]
        result = CubeCasinoFormatter(winners).format()
        assert result == [
            "@uzi won !hello from @ella and !damn from @future",
            "@eno won !8bitrickroll from @ella",
        ]
