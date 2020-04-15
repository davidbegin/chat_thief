from pathlib import Path
import traceback
from collections import Counter
from itertools import chain

from tinydb import TinyDB, Query

from chat_thief.models import User, SoundEffect, CommandPermission
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.irc import send_twitch_msg
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee



TABLE_NAME = "command_permissions"

db_location="db/soundeffects.json"

def _command_permissions_table(db_location):
    soundeffects_db_path = Path(__file__).parent.parent.parent.joinpath(db_location)
    return TinyDB(soundeffects_db_path).table(TABLE_NAME)

table = _command_permissions_table(db_location)

def leaderboard():
    result = table.search(
        Query().permitted_users
    )

    print(f"\n\nResult: {result}\n\n")

    # Sometimes we have multiples for the same command
    count = Counter(list(chain.from_iterable( [ command["permitted_users"] for command in result ])))

    # TODO: Format this better
    return str(count)
