import pytest

from pathlib import Path

from chat_thief.new_commands.pokemon_casino import PokemonCasino
from tests.support.database_setup import DatabaseConfig
from chat_thief.new_commands.pokemon_casino import PokemonCasino


class TestPokemonCasino(DatabaseConfig):
    @pytest.fixture(autouse=True)
    def clean_guess(self):
        PokemonCasino.GUESS_PATH = Path(__file__).parent.parent.joinpath(
            "tmp/pokeguess"
        )
        if PokemonCasino.GUESS_PATH.exists():
            PokemonCasino.GUESS_PATH.unlink()

    def test_starting_a_challenge(self):
        PokemonCasino.whos_that_pokemon()
