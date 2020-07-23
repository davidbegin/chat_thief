import shutil
from pathlib import Path

# import wikipedia
import pywikibot

from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary

all_sfx = SoundeffectsLibrary.fetch_soundeffect_names()

geo_guesser_countries = [
    "botswana",
    "senegal",
    "south africa",
    "bangladesh",
    "cambodia",
    "india",
    "indonesia",
    "israel",
    "japan",
    "malaysia",
    "mongolia",
    "philippines",
    "russia",
    "singapore",
    "taiwan",
    "thailand",
    "belgium",
    "bulgaria",
    "croatia",
    "denmark",
    "estonia",
    "finland",
    "france",
    "germany",
    "greece",
    "hungary",
    "iceland",
    "ireland",
    "italy",
    "latvia",
    "lithuania",
    "luxembourg",
    "netherlands",
    "norway",
    "poland",
    "portugal",
    "romania",
    "serbia",
    "slovakia",
    "slovenia",
    "spain",
    "sweden",
    "switzerland",
    "turkey",
    "ukraine",
    "united kingdom",
    "canada",
    "greenland",
    "mexico",
    "united states",
    "australia",
    "new zealand",
    "argentina",
    "bolivia",
    "brazil",
    "chile",
    "colombia",
    "ecuador",
    "peru",
    "Uruguay",
]

if __name__ == "__main__":

    for country in geo_guesser_countries:
        site = pywikibot.Site()
        page = pywikibot.Page(site, country)

        breakpoint()
    # existing_sounds = [ country for country in geo_guesser_countries if country in all_sfx ]

    # # sounds_folder = Path(__file__).parent.parent.joinpath("geoboard/sounds").resolve()
    # sounds_folder = Path("/home/begin/code/geoboard/sounds")
    # # sounds_folder = Path(__file__).parent.parent / "geoboard/sounds"


    # for sound in existing_sounds:
    #     soundpath = SoundeffectsLibrary.find_sample(sound)
    #     dest = sounds_folder.joinpath(soundpath.name)
    #     print(f"Copying Sound {soundpath.name} to {dest}")
    #     shutil.copy2(soundpath, dest)
