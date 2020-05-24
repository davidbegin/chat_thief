import pytest

from chat_thief.models.cube_bet import CubeBet
from chat_thief.routers.cube_casino_router import CubeCasinoRouter
from chat_thief.welcome_committee import WelcomeCommittee
from tests.support.database_setup import DatabaseConfig


class TestCubeCasinoRouter(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def mock_present_users(self, monkeypatch):
        def _mock_present_users(self):
            return ["future", "uzi"]

        monkeypatch.setattr(WelcomeCommittee, "present_users", _mock_present_users)

    def test_all_bets(self):
        result = CubeCasinoRouter("beginbotbot", "all_bets").route()
        assert result == ""
        assert CubeBet.count() == 0
        CubeCasinoRouter("random_user", "bet", ["42"]).route()
        result = CubeCasinoRouter("beginbotbot", "all_bets").route()
        assert result == "@random_user: 42"

    def test_bet(self):
        CubeCasinoRouter("beginbotbot", "all_bets").route()
        assert CubeBet.count() == 0
        result = CubeCasinoRouter("random_user", "bet", ["42"]).route()
        assert result == "Thank you for your bet: @random_user: 42s"
        assert CubeBet.count() == 1

    def test_cubed(self, mock_present_users):
        CubeCasinoRouter("future", "bet", ["108"]).route()
        CubeCasinoRouter("uzi", "bet", ["32"]).route()
        assert CubeBet.count() == 2
        result = CubeCasinoRouter("beginbotbot", "cubed", ["41"]).route()
        assert CubeBet.count() == 0
        assert result == ["Winner: @uzi Won 1 commands"]

    def test_cubed_with_a_timestamp(self, mock_present_users):
        CubeCasinoRouter("future", "bet", ["108"]).route()
        CubeCasinoRouter("uzi", "bet", ["32"]).route()
        assert CubeBet.count() == 2
        result = CubeCasinoRouter("beginbotbot", "cubed", ["00:00:41"]).route()
        assert CubeBet.count() == 0
        assert result == ["Winner: @uzi Won 1 commands"]

    def test_new_cube(self):
        CubeCasinoRouter("future", "bet", ["108"]).route()
        CubeCasinoRouter("uzi", "bet", ["32"]).route()
        assert CubeBet.count() == 2
        result = CubeCasinoRouter("beginbotbot", "new_cube", []).route()
        assert CubeBet.count() == 0
