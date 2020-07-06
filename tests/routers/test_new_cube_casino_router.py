import pytest

from chat_thief.models.cube_bet import CubeBet
from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.routers.new_cube_casino_router import NewCubeCasinoRouter
from tests.support.database_setup import DatabaseConfig


class TestCubeCasinoRouter(DatabaseConfig):

    # !bet 45 (implies choosing random sound)
    def test_simple_bet(self):
        User("wayne.shorter").save()
        Command("smooth").allow_user("wayne.shorter")
        result = NewCubeCasinoRouter("wayne.shorter", "bet", ["42"]).route()
        assert CubeBet.count() == 1
        last_bet = CubeBet.last()
        assert last_bet["wager"] == ["smooth"]
        assert last_bet["user"] == "wayne.shorter"
        result = NewCubeCasinoRouter("beginbotbot", "all_bets").route()
        assert result == "@wayne.shorter: 42"

    # !bet 45 clap damn
    def test_best_with_multiple_commands(self):
        User("wayne.shorter").save()
        User("grant.green").save()

        Command("smooth").allow_user("wayne.shorter")
        Command("damn").allow_user("wayne.shorter")
        Command("handbag").allow_user("grant.green")

        # Why did I have to bet directly???
        result = NewCubeCasinoRouter("grant.grant", "bet", ["32", "handbag"]).route()
        result = NewCubeCasinoRouter(
            "wayne.shorter", "bet", ["42", "smooth", "damn"]
        ).route()

        # assert CubeBet.count() == 2
        # last_bet = CubeBet.last()
        # assert last_bet["wager"] == ["smooth", "damn"]
        # assert last_bet["user"] == "wayne.shorter"
        # result = NewCubeCasinoRouter("beginbotbot", "all_bets").route()
        # assert "@wayne.shorter: 42" in result
        # assert "@grant.grant: 32" in result

        result = NewCubeCasinoRouter("beginbotbot", "cubed", ["42"]).route()
        assert result == ["@wayne.shorter won !handbag from @grant.grant"]
