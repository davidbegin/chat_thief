from pathlib import Path

import pytest

from chat_thief.models.user import User
from chat_thief.models.command import Command
from chat_thief.routers.pokemon_casino_router import PokemonCasinoRouter
from chat_thief.new_commands.pokemon_casino import PokemonCasino

from tests.support.database_setup import DatabaseConfig


class TestPokemonCasinoRouter(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def clean_guess(self):
        PokemonCasino.MYSTERY_POKEMON_PATH = Path(__file__).parent.parent.joinpath(
            "tmp/pokeguess"
        )
        if PokemonCasino.MYSTERY_POKEMON_PATH.exists():
            PokemonCasino.MYSTERY_POKEMON_PATH.unlink()
        PokemonCasino.GUESSES_PATH = Path(__file__).parent.parent.joinpath(
            "tmp/guesses"
        )
        if PokemonCasino.GUESSES_PATH.exists():
            PokemonCasino.GUESSES_PATH.unlink()

    def test_pokemon(self):
        result = PokemonCasinoRouter("beginbot", "pokemon", []).route()
        assert result == "Guess Which Pokemon This Is!!!"
        result = PokemonCasinoRouter("beginbot", "pokemon", []).route()
        assert result == "Who's that Pokemon"

    def test_guess_pokemon(self):
        result = PokemonCasinoRouter("beginbot", "pokemon", []).route()
        pokemon = PokemonCasino.MYSTERY_POKEMON_PATH.read_text()
        bad_guess = PokemonCasinoRouter("beginbot", "guess", ["caterpie"]).route()
        assert bad_guess == "@beginbot YOU WERE WRONG"
        good_guess = PokemonCasinoRouter("beginbot", "guess", [pokemon]).route()
        assert f"beginbot Won! {pokemon}" in good_guess

    def test_replay(self):
        result = PokemonCasinoRouter("beginbot", "pokemon", []).route()
        result = PokemonCasinoRouter("beginbot", "replay", []).route()
        assert result == "Who's that Pokemon"
