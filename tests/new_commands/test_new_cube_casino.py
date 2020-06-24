import pytest
import random

from chat_thief.models.command import Command
from chat_thief.models.cube_bet import CubeBet
from chat_thief.new_commands.new_cube_casino import NewCubeCasino
from tests.support.database_setup import DatabaseConfig


class TestNewCubeCasino(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def control_the_chaos(self):
        random.seed(0)

    def test_with_exact_winers(self):
        CubeBet("uzi", 45, ["damn"]).save()
        CubeBet("ella", 38, ["8bitrickroll", "hello"]).save()
        CubeBet("miles", 36, ["handbag"]).save()
        result = NewCubeCasino(45).gamble()
        assert result == [("uzi", "ella", "8bitrickroll")]

    def test_with_expensive_command_exact_match(self):
        Command("damn").save()
        Command("damn").set_value("cost", 10)
        CubeBet("uzi", 45, ["damn"]).save()
        CubeBet("ella", 38, ["8bitrickroll", "hello"]).save()
        CubeBet("miles", 36, ["handbag"]).save()
        result = NewCubeCasino(45).gamble()
        assert result == [
            ("uzi", "ella", "8bitrickroll"),
            ("uzi", "miles", "handbag"),
            ("uzi", "ella", "hello"),
        ]

    def test_expensive_command(self):
        Command("damn").save()
        Command("damn").set_value("cost", 10)
        CubeBet("uzi", 45, ["damn"]).save()
        CubeBet("ella", 38, ["8bitrickroll", "hello"]).save()
        CubeBet("miles", 36, ["handbag"]).save()
        result = NewCubeCasino(37).gamble()
        assert result == [
            ("miles", "ella", "hello"),
        ]

    def test_with_multiple_winners(self):
        CubeBet("ella", 45, ["8bitrickroll", "hello"]).save()
        CubeBet("uzi", 36, ["damn"]).save()
        CubeBet("miles", 36, ["handbag"]).save()
        result = NewCubeCasino(37).gamble()
        assert result == [("uzi", "ella", "hello"), ("miles", "ella", "8bitrickroll")]
