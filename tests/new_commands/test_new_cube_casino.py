import pytest

from chat_thief.models.cube_bet import CubeBet
from chat_thief.new_commands.new_cube_casino import NewCubeCasino
from tests.support.database_setup import DatabaseConfig


class TestNewCubeCasino(DatabaseConfig):
    def test_with_exact_winers(self):
        CubeBet("uzi", 45, ["damn"]).save()
        CubeBet("ella", 38, ["8bitrickroll", "hello"]).save()
        result = NewCubeCasino(45).gamble()
        assert result == [("uzi", "ella", "hello")]
