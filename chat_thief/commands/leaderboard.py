from pathlib import Path

import traceback
from collections import Counter
from itertools import chain

from tinydb import TinyDB, Query

from chat_thief.models.soundeffect import SoundEffect
from chat_thief.models.command_permission import CommandPermission

from chat_thief.config.stream_lords import STREAM_LORDS
from chat_thief.irc import send_twitch_msg
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.models.database import db_table, COMMANDS_DB_PATH


def loserboard():
    table = db_table(COMMANDS_DB_PATH, "commands")
    result = table.search(Query().permitted_users)

    counter = Counter(
        list(chain.from_iterable([command["permitted_users"] for command in result]))
    )

    def sort_users(user_commands):
        used, count = user_commands
        return count

    counter_values = counter.values()
    sorted_counter = sorted(counter.items(), key=sort_users)
    for user, count in sorted_counter[0:5]:
        send_twitch_msg(f"@{user} | {count} soundeffects")


def leaderboard():
    table = db_table(COMMANDS_DB_PATH, "commands")
    result = table.search(Query().permitted_users)

    counter = Counter(
        list(chain.from_iterable([command["permitted_users"] for command in result]))
    )
    # Most Common sorting alphabetically
    print(f"\nLeader board: {counter}\n")
    for user, count in counter.most_common()[0:5]:
        send_twitch_msg(f"@{user} | {count} soundeffects")
