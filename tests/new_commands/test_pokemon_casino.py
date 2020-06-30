import pytest

from pathlib import Path

from chat_thief.new_commands.pokemon_casino import PokemonCasino
from tests.support.database_setup import DatabaseConfig
from chat_thief.new_commands.pokemon_casino import PokemonCasino


class TestPokemonCasino(DatabaseConfig):
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

    def test_starting_a_challenge(self):
        result = PokemonCasino.whos_that_pokemon()
        assert result == "Guess Which Pokemon This Is!!!"
        pokemon = PokemonCasino.MYSTERY_POKEMON_PATH.read_text()
        assert pokemon is not None
        result = PokemonCasino.guess_pokemon("ash", "psyduck")
        "@ash YOU WERE WRONG"
        assert PokemonCasino.guesses() == 1
