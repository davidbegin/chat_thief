from pathlib import Path

import traceback
from collections import Counter
from itertools import chain

from tinydb import TinyDB, Query

from chat_thief.models import SoundEffect, CommandPermission
from chat_thief.stream_lords import STREAM_LORDS
from chat_thief.irc import send_twitch_msg
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.welcome_committee import WelcomeCommittee
from chat_thief.database import db_table, COMMANDS_DB_PATH


def leaderboard():
    table = db_table(COMMANDS_DB_PATH, "commands")
    result = table.search(
        Query().permitted_users
    )

    print(f"\n\nResult: {result}\n\n")

    counter = Counter(list(chain.from_iterable( [ command["permitted_users"] for command in result ])))
    for user, count in counter.most_common()[0:5]:
        send_twitch_msg(f"@{user} | {count} soundeffects")
