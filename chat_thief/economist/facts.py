from pathlib import Path
import traceback
from collections import Counter
from itertools import chain

from tinydb import TinyDB, Query

from chat_thief.models.user import User
from chat_thief.soundeffects_library import SoundeffectsLibrary
from chat_thief.models.vote import Vote
from chat_thief.models.command import Command


class Facts:
    def peace_count(self):
        vote = Vote("beginbot")
        return vote.peace_count()

    def revolution_count(self):
        vote = Vote("beginbot")
        return vote.revolution_count()

    def total_votes(self):
        return Vote("beginbot").vote_count()

    def available_sounds(self):
        return Command.count()

    def unavailable_sounds(self):
        total_sfx = len(SoundeffectsLibrary.soundeffects_only())
        return total_sfx - self.available_sounds()

    def cool_points(self):
        total_cool_points = User("beginbot").total_cool_points()
        return total_cool_points

    def street_cred(self):
        total_street_cred = User("beginbot").total_street_cred()
        return total_street_cred

    def top_users(self):
        result = Command.db().all()

        counter = Counter(
            list(
                chain.from_iterable([command["permitted_users"] for command in result])
            )
        )
        return counter.most_common()[0:5]
