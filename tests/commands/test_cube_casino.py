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
        assert subject._winners() == (107, ["gucci.mane"])

        CubeBet("playboi.carti", 109).save()
        assert subject._winners() == (107, ["gucci.mane"])

    def test_exact_winner(self):
        solve_time = 108
        subject = CubeCasino(solve_time)
        assert subject._winners() == (None, [])

        CubeBet("erik.statie", 420).save()
        CubeBet("playboi.carti", 108).save()
        assert subject._winners() == (108, ["playboi.carti"])

    def test_over_winner(self):
        solve_time = 108
        subject = CubeCasino(solve_time)
        assert subject._winners() == (None, [])

        CubeBet("erik.statie", 420).save()
        CubeBet("playboi.carti", 109).save()
        assert subject._winners() == (109, ["playboi.carti"])
