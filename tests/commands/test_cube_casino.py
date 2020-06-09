import pytest

from chat_thief.commands.cube_casino import CubeCasino
from chat_thief.models.cube_bet import CubeBet

from tests.support.database_setup import DatabaseConfig


class TestCubeCasino(DatabaseConfig):
    def test__winners(self):
        solve_time = 108
        subject = CubeCasino(solve_time)
        assert subject._winners() == (None, [])
        CubeBet("erik.statie", 420).save()

        CubeBet("gucci.mane", 107).save()
        winning_duration, winners, all_bets = subject._winners()
        assert winning_duration == 107
        assert winners == ["gucci.mane"]

        CubeBet("playboi.carti", 109).save()
        winning_duration, winners, all_bets = subject._winners()
        assert winning_duration == 107
        assert winners == ["gucci.mane"]

    def test_exact_winner(self):
        solve_time = 108
        subject = CubeCasino(solve_time)
        result = subject._winners()
        assert subject._winners() == (None, [])

        CubeBet("erik.statie", 420).save()
        CubeBet("playboi.carti", 108).save()
        winning_duration, winners, all_bets = subject._winners()
        assert winning_duration == 108
        assert winners == ["playboi.carti"]

    def test_over_winner(self):
        solve_time = 108
        subject = CubeCasino(solve_time)
        result = subject._winners()
        assert subject._winners() == (None, [])

        CubeBet("erik.statie", 420).save()
        CubeBet("playboi.carti", 109).save()
        result = subject._winners()
        winning_duration, winners, all_bets = subject._winners()
        assert winning_duration == 109
        assert winners == ["playboi.carti"]
