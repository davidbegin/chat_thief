from pathlib import Path
import traceback
from collections import Counter
from itertools import chain

from tinydb import TinyDB, Query

from chat_thief.models.database import db_table, COMMANDS_DB_PATH
from chat_thief.models.user import User


class Facts:

    def cool_points(self):
        total_cool_points = User("beginbot").total_cool_points()
        return total_cool_points

    def top_users(self):
        table = db_table(COMMANDS_DB_PATH, "commands")
        result = table.search(Query().permitted_users)

        counter = Counter(
            list(chain.from_iterable([command["permitted_users"] for command in result]))
        )
        return counter.most_common()[0:5]
        # [('blueredbrackets', 35), ('whatsinmyopsec', 13), ('zerostheory', 13), ('stupac62', 11), ('zanuss', 10)]
