from pathlib import Path

import os
import random

from chat_thief.audioworld.audio_player import AudioPlayer
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary
from chat_thief.begin_fund import BeginFund
from chat_thief.config.stream_lords import STREAM_GODS
from chat_thief.models.notification import Notification

POKEMON_NAMES = [
    "bulbasaur",
    "ivysaur",
    "venusaur",
    "charmander",
    "charmeleon",
    "charizard",
    "squirtle",
    "wartortle",
    "blastoise",
    "caterpie",
    "metapod",
    "butterfree",
    "weedle",
    "kakuna",
    "beedrill",
    "pidgey",
    "pidgeotto",
    "pidgeot",
    "rattata",
    "raticate",
    "spearow",
    "fearow",
    "ekans",
    "arbok",
    "pikachu",
    "raichu",
    "sandshrew",
    "sandslash",
    "nidoran-f",
    "nidorina",
    "nidoqueen",
    "nidoran-m",
    "nidorino",
    "nidoking",
    "clefairy",
    "clefable",
    "vulpix",
    "ninetales",
    "jigglypuff",
    "wigglytuff",
    "zubat",
    "golbat",
    "oddish",
    "gloom",
    "vileplume",
    "paras",
    "parasect",
    "venonat",
    "venomoth",
    "diglett",
    "dugtrio",
    "meowth",
    "persian",
    "psyduck",
    "golduck",
    "mankey",
    "primeape",
    "growlithe",
    "arcanine",
    "poliwag",
    "poliwhirl",
    "poliwrath",
    "abra",
    "kadabra",
    "alakazam",
    "machop",
    "machoke",
    "machamp",
    "bellsprout",
    "weepinbell",
    "victreebel",
    "tentacool",
    "tentacruel",
    "geodude",
    "graveler",
    "golem",
    "ponyta",
    "rapidash",
    "slowpoke",
    "slowbro",
    "magnemite",
    "magneton",
    "farfetchd",
    "doduo",
    "dodrio",
    "seel",
    "dewgong",
    "grimer",
    "muk",
    "shellder",
    "cloyster",
    "gastly",
    "haunter",
    "gengar",
    "onix",
    "drowzee",
    "hypno",
    "krabby",
    "kingler",
    "voltorb",
    "electrode",
    "exeggcute",
    "exeggutor",
    "cubone",
    "marowak",
    "hitmonlee",
    "hitmonchan",
    "lickitung",
    "koffing",
    "weezing",
    "rhyhorn",
    "rhydon",
    "chansey",
    "tangela",
    "kangaskhan",
    "horsea",
    "seadra",
    "goldeen",
    "seaking",
    "staryu",
    "starmie",
    "mr. mime",
    "scyther",
    "jynx",
    "electabuzz",
    "magmar",
    "pinsir",
    "tauros",
    "magikarp",
    "gyarados",
    "lapras",
    "ditto",
    "eevee",
    "vaporeon",
    "jolteon",
    "flareon",
    "porygon",
    "omanyte",
    "omastar",
    "kabuto",
    "kabutops",
    "aerodactyl",
    "snorlax",
    "articuno",
    "zapdos",
    "moltres",
    "dratini",
    "dragonair",
    "dragonite",
    "mewtwo",
    "mew",
]


class PokemonCasino:
    MYSTERY_POKEMON_PATH = Path(__file__).parent.parent.parent.joinpath("tmp/pokeguess")
    GUESSES_PATH = Path(__file__).parent.parent.parent.joinpath("tmp/guesses")

    @classmethod
    def guesses(cls):
        if cls.GUESSES_PATH.exists():
            return len(cls.GUESSES_PATH.read_text().strip().split("\n"))
        else:
            return 0

    @classmethod
    def replay(cls):
        print("Replaying Pokemon")

        if "TEST_MODE" not in os.environ:
            pokemon = cls.MYSTERY_POKEMON_PATH.read_text()
            soundfile = SoundeffectsLibrary.find_sample(pokemon)
            AudioPlayer.play_sample(soundfile.resolve(), notification=False)

        return "Who's that Pokemon"

    @classmethod
    def guess_pokemon(cls, user, guess):
        pokemon = cls.MYSTERY_POKEMON_PATH.read_text()

        print(f"@{user} guessed {guess}")

        if guess == pokemon:
            cls.MYSTERY_POKEMON_PATH.unlink()
            guess_count = cls.guesses()
            cls.GUESSES_PATH.unlink()

            result = f"{user} Won! {pokemon} - Beating {guess_count} Other People"
            prize = None

            if user not in STREAM_GODS:
                prize = BeginFund(target_user=user).dropeffect()

                result += f" | {prize}"

            if "TEST_MODE" not in os.environ:
                soundfile = SoundeffectsLibrary.find_sample("pokewin")
                AudioPlayer.play_sample(soundfile.resolve(), notification=False)

            Notification(f"{user} won: {guess}").save()
            return result
        else:
            with open(cls.GUESSES_PATH, "a") as f:
                f.write(f"{user}: {guess}\n")
            return f"@{user} YOU WERE WRONG"

    @classmethod
    def whos_that_pokemon(cls):
        if cls.MYSTERY_POKEMON_PATH.exists():
            return cls.replay()

        if "TEST_MODE" not in os.environ:
            soundfile = SoundeffectsLibrary.find_sample("pokewho")
            AudioPlayer.play_sample(soundfile.resolve())

        pokemon = random.sample(POKEMON_NAMES, 1)[0]

        if "TEST_MODE" not in os.environ:
            soundfile = SoundeffectsLibrary.find_sample(pokemon)
            AudioPlayer.play_sample(soundfile.resolve(), notification=False)

        with open(cls.MYSTERY_POKEMON_PATH, "w") as f:
            f.write(pokemon)

        return "Guess Which Pokemon This Is!!!"
