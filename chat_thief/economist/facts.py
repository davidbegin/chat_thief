from pathlib import Path
import traceback
from collections import Counter
from itertools import chain

from chat_thief.models.user import User
from chat_thief.audioworld.soundeffects_library import SoundeffectsLibrary
from chat_thief.models.vote import Vote
from chat_thief.models.command import Command
from chat_thief.models.breaking_news import BreakingNews


class Facts:
    def breaking_news(self):
        return BreakingNews.last()

    def most_popular(self):
        return Command.most_popular()

    def peace_count(self):
        vote = Vote("beginbot")
        return vote.peace_count()

    def revolution_count(self):
        vote = Vote("beginbot")
        return vote.revolution_count()

    def total_votes(self):
        return Vote.count()

    def available_sounds(self):
        return len(Command.available_sounds())

    def unavailable_sounds(self):
        total_sfx = len(SoundeffectsLibrary.soundeffects_only())
        return total_sfx - self.available_sounds()

    def total_sounds(self):
        return self.available_sounds() + self.unavailable_sounds()

    def cool_points(self):
        return User.total_cool_points()

    def street_cred(self):
        return User.total_street_cred()

    def top_users(self):
        result = Command.db().all()

        counter = Counter(
            list(
                chain.from_iterable([command["permitted_users"] for command in result])
            )
        )
        return counter.most_common()[0:5]
