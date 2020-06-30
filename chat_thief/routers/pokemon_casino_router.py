import datetime

from chat_thief.routers.base_router import BaseRouter
from chat_thief.models.user import User
from chat_thief.new_commands.pokemon_casino import PokemonCasino


class PokemonCasinoRouter(BaseRouter):
    def route(self):
        if self.command == "pokemon":
            return PokemonCasino.whos_that_pokemon()

        if self.command == "guess":
            if self.parser.target_command:
                return PokemonCasino.guess_pokemon(self.user, self.parser.target_sfx)
            else:
                return f"@{self.user} NOT A Valid Pokemon {self.args}"

        if self.command == "replay":
            return PokemonCasino.replay()
